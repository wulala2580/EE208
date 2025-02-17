'''Train CIFAR-10 with PyTorch.'''
import os

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from models import resnet20

start_epoch = 0
end_epoch = 4
lr = 0.1

# Data pre-processing, DO NOT MODIFY
print('==> Preparing data..')
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True)

testset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=False)

classes = ("airplane", "automobile", "bird", "cat",
           "deer", "dog", "frog", "horse", "ship", "truck")

# Model
print('==> Building model..')
model = resnet20()
# If you want to restore training (instead of training from beginning),
# you can continue training based on previously-saved models
# by uncommenting the following two lines.
# Do not forget to modify start_epoch and end_epoch.
# restore_model_path = 'pretrained/ckpt_4_acc_63.320000.pth'
# model.load_state_dict(torch.load(restore_model_path)['net'])

# A better method to calculate loss
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=lr, weight_decay=5e-4)

result = dict()
def train(epoch):
    model.train()
    train_loss = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(trainloader):
        optimizer.zero_grad()
        outputs = model(inputs)
        # The outputs are of size [128x10].
        # 128 is the number of images fed into the model 
        # (yes, we feed a certain number of images into the model at the same time, 
        # instead of one by one)
        # For each image, its output is of length 10.
        # Index i of the highest number suggests that the prediction is classes[i].
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        print('Epoch [%d] Batch [%d/%d] Loss: %.3f | Training Acc: %.3f%% (%d/%d)'
              % (epoch, batch_idx + 1, len(trainloader), train_loss / (batch_idx + 1),
                 100. * correct / total, correct, total))

def test(epoch):
    print('==> Testing...')
    global best_acc
    model.eval()
    test_loss = 0
    correct = 0
    total = 0
    result[epoch] = []
    with torch.no_grad():
        ##### TODO: calc the test accuracy #####
        # Hint: You do not have to update model parameters.
        #       Just get the outputs and count the correct predictions.
        #       You can turn to `train` function for help.
        for batch_idx, (inputs, targets) in enumerate(testloader):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            test_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
            print('Epoch [%d] Batch [%d/%d] Loss: %.3f | Testing Acc: %.3f%% (%d/%d)'
                  % (epoch, batch_idx + 1, len(testloader), test_loss / (batch_idx + 1),
                     100. * correct / total, correct, total))
            if batch_idx + 1 == len(testloader):
                result[epoch] = 100. * correct / total
        acc = 100. * correct / total
        ########################################
    # Save checkpoint.
    print('Test Acc: %f' % acc)
    print('Saving..')
    state = {
        'net': model.state_dict(),
        'acc': acc,
        'epoch': epoch,
    }
    if not os.path.isdir('checkpoint'):
        os.mkdir('checkpoint')
    torch.save(state, './checkpoint/ckpt_%d_acc_%f.pth' % (epoch, acc))

for epoch in range(start_epoch, end_epoch + 1):
    train(epoch)
    test(epoch)

optimizer = optim.SGD(model.parameters(), lr=0.01, weight_decay=5e-4)
for epoch in range(end_epoch+1, end_epoch + 6):
    train(epoch)
    test(epoch)

print result
