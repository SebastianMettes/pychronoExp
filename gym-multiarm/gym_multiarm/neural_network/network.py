import shutil
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


import os




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
            nn.ReLU(),
            nn.Linear(hidden_size,n_actions)
        )

    def forward(self, x):
        return self.Net(x)

    def load_model(self,version_path):
        self.Net.load_state_dict(torch.load(version_path))

    def save_model(self,directory_path):
        tmp_name = directory_path+'_tmp'
        if os.path.isdir(directory_path) == False:
            os.mkdir(tmp_name, mode = 0o777)
        torch.save(self.Net.state_dict(),os.path.join(tmp_name,'model.pt'))
        shutil.move(tmp_name,directory_path)




    









    pass
