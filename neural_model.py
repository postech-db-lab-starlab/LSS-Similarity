import torch
import torch.nn as nn

class NeuralClassifier(nn.Module):
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