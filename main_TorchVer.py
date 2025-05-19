import statistics

import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import math
import numpy as np
from torch.utils.data import Dataset, DataLoader

import las_files as las
import parsing as pars

window_size = 200
window_step = 100 #15 fits the best
# Shared feature extractor (MLP for 1D inputs)
class LogEncoder(nn.Module):
    def __init__(self, input_size):
        super(LogEncoder, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64)
        )

    def forward(self, x):
        return self.net(x)

# Siamese Network
class SiameseNet(nn.Module):
    def __init__(self, input_size):
        super(SiameseNet, self).__init__()
        self.encoder = LogEncoder(input_size)

    def forward(self, x1, x2):
        z1 = self.encoder(x1)
        z2 = self.encoder(x2)
        # L2 distance between feature vectors
        distance = F.pairwise_distance(z1, z2)
        return distance

class ContrastiveLoss(nn.Module):
    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, distance, label):
        loss = (label) * distance.pow(2) + \
               (1 - label) * F.relu(self.margin - distance).pow(2)
        return loss.mean()


# Dummy dataset: пары окон и метки
class WellLogPairs(Dataset):
    def __init__(self, X1, X2, y):
        self.X1 = torch.tensor(X1, dtype=torch.float32)
        self.X2 = torch.tensor(X2, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X1)

    def __getitem__(self, idx):
        return self.X1[idx], self.X2[idx], self.y[idx]

# Разбиение на окна

injector = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_7276_inj.las")
well3894 = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_3894.las", False, injector)
well8480 = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_8480.las", False, injector)
well24402 = pars.parse_transformation("D:\Python\Abai\\2 cell\GR_24402.las", False, injector)
well2389 = pars.parse_transformation("D:\Python\Abai\\2 cell\GR_2389.las", False, injector)


wells = [injector, well3894, well8480, well24402, well2389]
cutted = las.cut_depth_wells(wells)
cutted_to_np = las.cutted_to_np(cutted)

X1_train, X2_train, y = pars.prepare_train_data(cutted_to_np[1:3], cutted_to_np[0], window_size, window_step, pos=True)
X1_train_neg, X2_train_neg, y_neg = pars.prepare_train_data(cutted_to_np[3:5], cutted_to_np[0], window_size, window_step, pos=False)

# Объединяем
X1_all = np.vstack([X1_train, X1_train_neg])
X2_all = np.vstack([X2_train, X2_train_neg])
y_all = np.concatenate([y, y_neg])

dataset = WellLogPairs(X1_all, X2_all, y_all)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

model = SiameseNet(input_size=window_size)
criterion = ContrastiveLoss(margin=1.0)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(10):
    total_loss = 0
    for x1, x2, label in loader:
        optimizer.zero_grad()
        dist = model(x1, x2)
        loss = criterion(dist, label)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

pars.print_window_size(X2_train)
for cutted_well in cutted_to_np:
    X1_val = pars.create_windows(cutted_well, window_size, window_step)
    #print(X1_val[0:1])
    #print(X2_train[0:1])
    sum_percentages = 0
    count_percent = 0
    for i, window in enumerate(X1_val):
        model.eval()
        with torch.no_grad():
            sample1 = torch.tensor(window, dtype=torch.float32)
            sample2 = torch.tensor(X2_train[i:i+1], dtype=torch.float32)
            distance = euclidean(cutted_to_np[0], cutted_to_np[1])
            percentage = 1 / math.exp(distance) * 100
            sum_percentages += percentage
            count_percent += 1
            ##print(f"Distance: {distance:.4f} (lower = more similar)")
            #print(f"Similarity: {percentage:.2f}% (higher = more similar)")
    average_percentage = sum_percentages / count_percent
    print(f"Average similarity: {average_percentage:.2f}% (higher = more similar)")



