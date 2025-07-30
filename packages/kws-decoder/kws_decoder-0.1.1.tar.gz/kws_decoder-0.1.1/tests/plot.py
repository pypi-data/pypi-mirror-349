import json

import matplotlib.pyplot as plt
import numpy as np
import torch

plt.rcParams["figure.figsize"] = (50, 5)

with open('resources/labels.json') as f:
    labels = json.load(f)
labels[0] = 'blank'
labels[-1] = 'space'

data = torch.load('resources/output.pth')
data = data.squeeze().numpy()

for i, label in enumerate(labels):
    plt.plot(range(data.shape[0]), data[:, i], label=label)
plt.legend(labels, ncol=4)

plt.savefig('output.png')
