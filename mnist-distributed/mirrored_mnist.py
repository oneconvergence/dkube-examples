import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tensorflow import keras
from tensorflow.keras import layers
from mlflow import log_metric
import gzip, pickle, os
import numpy as np
import tensorflow as tf
import argparse

MODEL_DIR = "/model/"
input_shape = (28, 28, 1)
num_classes = 10

def data_loader(hyperparams):
    f = gzip.open('/mnist/mnist.pkl.gz', 'rb')
    dataset = pickle.load(f, encoding='bytes')
    f.close()
    (x_train, y_train), (x_test, y_test) = dataset
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    #Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    
    return (
        tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(hyperparams['BATCH_SIZE']),
        tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(hyperparams['BATCH_SIZE']),
    )
    
def model_with_strategy(learning_rate):
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        model = keras.Sequential(
                [
                    keras.Input(shape=input_shape),
                    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
                    layers.MaxPooling2D(pool_size=(2, 2)),
                    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                    layers.MaxPooling2D(pool_size=(2, 2)),
                    layers.Flatten(),
                    layers.Dropout(0.5),
                    layers.Dense(num_classes, activation="softmax"),
                ]
            )
        model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(learning_rate), metrics=["accuracy"])
    return model
  
class DistributedTrainingMnistClassification(object):
    def __init__(self, learning_rate=0.01, batch_size=64, epochs=2):
        hyperparams = {'BUFFER_SIZE': 10000, 'BATCH_SIZE': batch_size}
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.train_dataset, self.test_dataset = data_loader(hyperparams)
        
    def train(self):
        model = model_with_strategy(self.learning_rate)
        #steps per epoch are reduced here to train on limited resources
        #you are free to remove this argument
        history = model.fit(self.train_dataset, 
                            epochs=self.epochs,
                            shuffle=True,
                            steps_per_epoch=30,
                            validation_data=self.test_dataset,
                            validation_steps=30,
                            verbose=0)
        
        tf.saved_model.save(model,MODEL_DIR + str(1))
        val_losses = history.history['val_loss']
        val_accuracies = history.history['val_accuracy']
        for epoch, val_loss, val_accuracy in zip(range(self.epochs), val_losses, val_accuracies):
          print("epoch {}:\nval_loss={:.2f}\nval_accuracy={:.2f}\n".format(epoch + 1, val_loss, val_accuracy))
          
          
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-lr", "--learning_rate", default="1e-4", help="Learning rate for the Keras optimizer")
    parser.add_argument("-bsz", "--batch_size", default="64", help="Batch size for each step of learning")
    parser.add_argument("-e", "--epochs", default="2", help="Number of epochs in each trial")
    args = parser.parse_args()
    learning_rate = float(args.learning_rate)
    batch_size = int(args.batch_size)
    epochs = int(args.epochs)
    model = DistributedTrainingMnistClassification(learning_rate, batch_size, epochs)
    model.train()
