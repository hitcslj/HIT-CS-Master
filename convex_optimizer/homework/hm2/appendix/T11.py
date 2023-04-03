import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from torch.utils.data import DataLoader
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Modify ResNet-18 to extract activations
class ResNet18Activations(nn.Module):
    def __init__(self, resnet18, target_layer):
        super(ResNet18Activations, self).__init__()
        self.features = nn.Sequential(*list(resnet18.children())[:target_layer])

    def forward(self, x):
        x = self.features(x)
        return x

# Load pre-trained ResNet-18 model
resnet18 = models.resnet18(pretrained=True)
resnet18_activations = ResNet18Activations(resnet18, 5)

# Data normalization and augmentation (optional)
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

# Load CIFAR-10 dataset
cifar10_train = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
cifar10_test = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

# Create DataLoader objects
batch_size = 100
train_loader = DataLoader(cifar10_train, batch_size=batch_size, shuffle=True, num_workers=0)
test_loader = DataLoader(cifar10_test, batch_size=batch_size, shuffle=False, num_workers=0)

# Extract activations
activations_list = []
for data, target in train_loader:
    activations = resnet18_activations(data)
    activations_list.append(activations.cpu().detach().numpy())

# Concatenate and reshape the activations
activations_array = np.concatenate(activations_list)
reshaped_activations = activations_array.reshape(len(activations_array), -1)

# Apply PCA
pca = PCA(n_components=2)
low_dim_data_pca = pca.fit_transform(reshaped_activations)

# Apply t-SNE
tsne = TSNE(n_components=2, perplexity=30, learning_rate=200, n_iter=1000)
low_dim_data_tsne = tsne.fit_transform(reshaped_activations)

# Visualize the low-dimensional representation of the activations using PCA
plt.figure()
plt.scatter(low_dim_data_pca[:, 0], low_dim_data_pca[:, 1], alpha=0.5)
plt.title("PCA")
plt.show()
plt.savefig("pca.png")

# Visualize the low-dimensional representation of the activations using t-SNE
plt.figure()
plt.scatter(low_dim_data_tsne[:, 0], low_dim_data_tsne[:, 1], alpha=0.5)
plt.title("t-SNE")
plt.show()
plt.savefig("tsne.png")
