import torch
import torch.nn as nn
import torch.optim as optim

import numpy as np

class NeuralClassifier(nn.Module):
    def __init__(self,
                 num_epoch=100,
                 lr=1e-3):
        super(NeuralClassifier, self).__init__()

        self.num_epoch = num_epoch
        self.lr = lr

        self.network = NeuralModel(3, 10, 1)

        self.criterion = nn.BCELoss()
        self.optimizer = optim.Adam(self.network.parameters(), lr=self.lr)

    def forward(self, x):
        result = self.network(x)
        return result

    def train(self, x, targets):
        if not isinstance(x, torch.Tensor):
            x = torch.Tensor(x)
        if not isinstance(targets, torch.Tensor):
            targets = torch.Tensor(targets)

        self.train()
        for epoch in range(self.num_epoch):
            self.optimizer.zero_grad()

            outputs = self.network(x)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.backward()

    def predict(self, x):
        if not isinstance(x, torch.Tensor):
            x = torch.Tensor(x)

        return self(x).view(-1).detach().cpu().nunpy()


class NeuralModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, target_size):
        super(NeuralClassifier, self).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.target_size = target_size

        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
            nn.Linear(hidden_dim, target_size)
        )

    def forward(self, x):
        return self.network(x)