import torch
import torch.nn as nn
import torch.nn.functional as F




class cross_entropy_agent(nn.Module):
    def __init__(self, obs_size,hidden_size, n_actions):
        """In the constructor, we instantiate 5 layers, including 3 hidden layers."""
        super().__init__()
        self.Net = nn.Sequential(
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
        return self.Net(x)

    def load_model(self,version_path):
        self.load_state_dict(torch.load(version_path))

    









    pass
