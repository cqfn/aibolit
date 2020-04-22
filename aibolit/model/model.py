import torch.nn as nn


class Maxout(nn.Module):

    def __init__(self, d_in, d_out, pool_size):
        super().__init__()
        self.d_in, self.d_out, self.pool_size = d_in, d_out, pool_size
        self.lin = nn.Linear(d_in, d_out * pool_size)

    def forward(self, inputs):
        shape = list(inputs.size())
        shape[-1] = self.d_out
        shape.append(self.pool_size)
        max_dim = len(shape) - 1
        out = self.lin(inputs)
        m, i = out.view(*shape).max(max_dim)
        return m


# this value was given during model evaluation
neurons_number = 50


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.f = nn.Sequential(
            Maxout(23, neurons_number, 2),
            Maxout(neurons_number, neurons_number, 2),
            nn.Linear(neurons_number, 1)
        )

    def forward(self, x):
        return self.f(x)
