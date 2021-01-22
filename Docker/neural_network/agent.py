import torch.nn as nn
import torch.nn.functional as F
import torch.nn.CrossEntropyLoss as CEL

HIDDEN_SIZE = 128
BATCH_SIZE = 256
PERCENTILE = 70


class cross_entropy_agent(nn.Module):
    def __init__(self, obs_size,hidden_size, n_actions):
        """In the constructor, we instantiate 5 layers, including 3 hidden layers."""
        super(cross_entropy_agent)
        self.cross_entropy_agent = nn.Sequential(
            nn.Linear(obs_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size,hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size,hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size,hidden_size),
            nn.ReLU(hidden_size),
            nn.Linear(hidden_size,n_actions)

        )
    def forward(self, x):
        return self.cross_entropy_agent(x)








    pass
