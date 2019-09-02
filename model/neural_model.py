import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

import pickle

class NeuralClassifier(nn.Module):
    def __init__(self,
                 objective="regression",
                 num_epoch=100,
                 hidden_dim=10,
                 lr=1e-3,
                 validation=True):
        super(NeuralClassifier, self).__init__()

        self.num_epoch = num_epoch
        self.lr = lr

        self.objective = objective

        if objective == "regression":
            self.network = NeuralRegressionModel(3, hidden_dim, 1)
            self.criterion = nn.BCELoss()
        elif objective == "classification":
            self.network = NeuralClassificationModel(3, hidden_dim, 2)
            self.criterion = nn.CrossEntropyLoss()
        
        self.optimizer = optim.Adam(self.network.parameters(), lr=self.lr)

        self.best_model = None
        self.validation = True

    def forward(self, x):
        result = self.network(x)
        return result

    def trainer(self, x, targets):
        if not isinstance(x, type(torch.Tensor)):
            x = torch.Tensor(x)
        if not isinstance(targets, torch.Tensor):
            targets = torch.Tensor(targets)

        train_len = int(len(x) * 0.8)
        train_x = x[:train_len]
        train_targets = targets[:train_len]
        val_x = x[train_len:]
        val_targets = targets[train_len:]

        self.train()
        prev_loss = 1e10
        for epoch in range(self.num_epoch):
            self.optimizer.zero_grad()

            outputs = self.network(train_x)
            loss = self.criterion(outputs, train_targets.view(-1, 1))
            loss.backward()
            self.optimizer.step()

            if self.validation:
                val_outputs = self.network(val_x)
                loss = self.criterion(val_outputs, val_targets.view(-1, 1))
                loss = float(loss)
                if loss < prev_loss:
                    self.best_model = pickle.dumps(self.network)
                    prev_loss = loss

        if self.validation:
            self.network = pickle.loads(self.best_model)

    def predict(self, x):
        if not isinstance(x, torch.Tensor):
            x = torch.Tensor(x)

        return self(x).view(-1).detach().cpu().numpy()


class NeuralRegressionModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, target_size):
        super(NeuralRegressionModel, self).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.target_size = target_size

        self.network = nn.Sequential(
            nn.BatchNorm1d(input_dim),
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, target_size),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


class NeuralClassificationModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, target_size):
        super(NeuralClassificationModel, self).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.target_size = target_size

        self.network = nn.Sequential(
            nn.BatchNorm1d(input_dim),
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, target_size),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.network(x)