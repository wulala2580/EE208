from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import torch

from models import Naive_NN


NUM_TRAIN_SAMPLES = 200
NUM_TRAIN_EPOCHS = 1000  # try: 100, 1000, 10000, 50000
LEARNING_RATE = 0.01

torch.manual_seed(2019)

def f(x):
    """Actual function (ground truth)."""
    # x**2 + 2 * np.sin(x) + np.cos(x - 1) - 5
    return x**2

# Create dataset


class MyDataset(torch.utils.data.Dataset):
    def __init__(self):
        super(MyDataset, self).__init__()
        self.x, self.y = self.generate_data(NUM_TRAIN_SAMPLES)

    def generate_data(self, num):
        # Generate num training data disturbed by noise.
        x = (torch.rand([num, 1]) - 0.5) * 10.0
        y_noise = f(x) + torch.randn([num, 1]) * 3
        return x, y_noise

    def get_all_data(self):
        return self.x.detach(), self.y.detach()

    def __len__(self):
        return NUM_TRAIN_SAMPLES

    def __getitem__(self, index):
        return self.x[index], self.y[index]


model = Naive_NN()
model.load_state_dict(torch.load('model.pth'))
dataset = MyDataset()
dataloader = torch.utils.data.DataLoader(dataset, batch_size=200, shuffle=True)
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

model.eval()
with torch.no_grad():
    x = torch.linspace(-5, 5, 50).reshape([50, 1])
    y = model(x)
    plt.plot(x, y, color='y', label='learnt curve')  # learnt curve
    plt.plot(x, f(x), color='r', label='ground-truth curve')  # ground-truth curve
    plt.scatter(*(dataset.get_all_data()), label='training set')  # training set
    plt.legend()
    plt.show()
    torch.save(model, 'model.pth')