# Train a model using chest x-ray images

import os
import numpy as np
import glob
import cv2
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf
from tensorflow import keras
import mlflow

image_types = ('.jpg', 'jpeg', '.png', '.svg')

# Ignore all warnings to clean up log file
import warnings
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()

# Set up parsing for the Katib inputs & image resize
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--epochs', type=int, default=5,
                        help='The number of epochs for training')
parser.add_argument('--learning_rate', type=float, default=0.01,
                        help="learning rate for optimizer")
parser.add_argument('--image_size',type=int, default=200,
                        help="Image resize value")
args = parser.parse_args()

# Set up input hyperparameters & size
NUM_EPOCHS = int(os.getenv("EPOCHS", args.epochs))
LEARNING_RATE = args.learning_rate
IMAGE_SIZE=args.image_size

print("NUM_EPOCHS =", NUM_EPOCHS)
print("LEARNING_RATE =", LEARNING_RATE)
print("IMAGE_SIZE =", IMAGE_SIZE)

# Image Data Functions

class ImageData():
    def __init__(self):
        pass

    def read_data_from_dir(self, imagedir, grayscale=True, read_labels=False):
        image_files = list()
        for file_type in image_types:
            image_files.extend(glob.glob(os.path.join(imagedir, "**/*" + file_type), recursive=True))
        if len(image_files) == 0:
            return None
        images = []
        for each_image_file in image_files:
            if grayscale:
                img = cv2.imread(each_image_file, cv2.IMREAD_GRAYSCALE)
            else:
                img = cv2.imread(each_image_file)
            if img is not None:
                images.append(img)
        train_x = np.asarray(images)
        if read_labels:
            csv_files = glob.glob(os.path.join(imagedir, "**/*" + ".csv"), recursive=True)
            label_data = pd.read_csv(csv_files[-1])
            train_y = label_data.iloc[:,-1:].values
            return train_x, train_y
        else:
            return train_x

    def read_classification_data(self, datadir):
        train_x = list()
        train_y = list()
        for dp, dn, filenames in os.walk(datadir):
            if len(filenames) > 0:
                current_class_data = self.read_data_from_dir(dp)
                train_x.extend(current_class_data)
                train_y.extend([os.path.basename(dp)] * current_class_data.shape[0])
        if len(train_x) == 0:
            return None
        train_x = np.asarray(train_x)
        train_y = np.asarray(train_y)
        train_y_classes, train_y = np.unique(train_y, return_inverse=True)
        return train_x, (train_y_classes, train_y)

    def resize_images(self, images, new_shape):
        resized_images = []
        for each_image in images:
            resized_images.append(cv2.resize(each_image, new_shape, interpolation= cv2.INTER_LINEAR))
        resized_images = np.asarray(resized_images)
        return resized_images

# Set up image variables
imd = ImageData()
train_x, train_y = imd.read_classification_data("/data")
train_y_classes, train_y = train_y
resized_train_x = imd.resize_images(train_x, (IMAGE_SIZE,IMAGE_SIZE))
resized_train_x = resized_train_x.reshape(resized_train_x.shape[0], IMAGE_SIZE, IMAGE_SIZE, 1)

encoder = OneHotEncoder(sparse=False)
onehot = encoder.fit_transform(train_y.reshape(-1, 1))

# Set up MLFlow Experiment
MLFLOW_EXPERIMENT_NAME = os.getenv('DKUBE_PROJECT_NAME')

if MLFLOW_EXPERIMENT_NAME:
    exp = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
    if not exp:
        print("Creating experiment...")
        mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
    mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT_NAME)

# Output directory for MLFlow
OUTPUT_MODEL_DIR = os.getcwd()+"/model_mlflow"
os.makedirs(OUTPUT_MODEL_DIR, exist_ok=True)

# MLFlow metric logging function
class loggingCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        mlflow.log_metric("train_loss", logs["loss"], step=epoch)
        mlflow.log_metric ("train_accuracy", logs["accuracy"], step=epoch)
        mlflow.log_metric("val_loss", logs["val_loss"], step=epoch)
        mlflow.log_metric ("val_accuracy", logs["val_accuracy"], step=epoch)
        # output accuracy metric for katib to collect from stdout
        print(f"loss={round(logs['loss'],2)}")
        print(f"val_loss={round(logs['val_loss'],2)}")
        print(f"accuracy={round(logs['accuracy'],2)}")
        print(f"val_accuracy={round(logs['val_accuracy'],2)}")

# Function to create & compile model
def create_model():
  model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(IMAGE_SIZE,IMAGE_SIZE,1)),
    tf.keras.layers.Conv2D(2, 4, strides=2, padding='same', activation=tf.nn.relu),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='linear'),
    tf.keras.layers.Dense(20, input_dim=5, activation='linear'),
    tf.keras.layers.Dense(10, activation='linear'),
    tf.keras.layers.Dense(4, activation='linear'),
    tf.keras.layers.Dense(2, activation='sigmoid')
    ])

  model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=LEARNING_RATE),
              loss='binary_crossentropy',
              metrics=['accuracy'])
  return model

# Create & train model and save metrics/artifacts & TensorBoard events
print("Create Model")
model = create_model()

# Set up folder for TensorBoard events
# The variable DKUBE_TENSORBOARD_DIR is where the TB UI will look for the event logs
DKUBE_TENSORBOARD_DIR = "/model/tensorboard"

# Training run with callbacks to log metrics and TensorBoard events
print("MLFlow Run")
with mlflow.start_run(run_name="xray") as run:
    model.fit(x=resized_train_x, y=onehot, epochs=NUM_EPOCHS, verbose=False, validation_split=0.1,
      callbacks=[loggingCallback(),
      tf.keras.callbacks.TensorBoard(log_dir=DKUBE_TENSORBOARD_DIR)]
      )

    # Print the accuracy & loss
    loss, acc = model.evaluate(resized_train_x,onehot, verbose=False)
    print("Training Accuracy = ", acc)
    print("Training Loss =", loss)

    # Create checkpoint file with trained model weights

    # Save checkpoint
    model.save_weights("chest-xray/checkpoint/xray-weights")

    # Export model & metrics
    print("Model Save")
    model.save("/model/1")

    print("Artifact Save")
    mlflow.log_artifacts(OUTPUT_MODEL_DIR)
    print("Log Model")
    mlflow.keras.log_model(keras_model=model, artifact_path=None)