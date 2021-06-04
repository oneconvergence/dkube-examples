import gzip, pickle, os
import numpy as np
import torch
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
from mlflow import log_metric
from net import Net
import shutil

# read env variables
epochs = int(os.getenv("EPOCHS","2"))
device = "cuda" if torch.cuda.is_available() else "cpu"
batch_size = 1280

#limit training on 1 core
torch.set_num_threads(1)

# Load dataset
f = gzip.open('/mnist/mnist.pkl.gz', 'rb')
data = pickle.load(f, encoding='bytes')
f.close()
(x_train, y_train), (x_test, y_test) = data

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, 1)
x_test = np.expand_dims(x_test, 1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

y_train = torch.from_numpy(y_train).type(torch.LongTensor)
y_test = torch.from_numpy(y_test).type(torch.LongTensor)

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        x = self.x[index]
        y = self.y[index]
        return (x,y)
train_loader = torch.utils.data.DataLoader(MyDataset(x_train,y_train), batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(MyDataset(x_test,y_test), batch_size=x_test.shape[0])

def train(model, device, train_loader, optimizer, epoch):
    model.train()

    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 10 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()),end='\r')
            step = (epoch - 1) * len(train_loader.dataset) + batch_idx * len(data)
            log_metric ("train_loss", loss.item(), step=step)

def test(model, device, test_loader, step):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))
        
    log_metric ("test_loss", test_loss, step=step)
    log_metric ("test_accuracy", 100. * correct / len(test_loader.dataset), step=step)

model = Net().to(device)
optimizer = optim.Adadelta(model.parameters(), lr=1.0)

scheduler = StepLR(optimizer, step_size=1, gamma=0.7)
for epoch in range(1, epochs + 1):
    train(model, device, train_loader, optimizer, epoch)
    step = (epoch) * len(train_loader.dataset)
    test(model, device, test_loader, step)
    scheduler.step()

torch.save(model.state_dict(), "/model/model.pt")
dirpath = os.path.dirname(os.path.abspath(__file__))
shutil.copy(dirpath + "/net.py","/model/net.py")
