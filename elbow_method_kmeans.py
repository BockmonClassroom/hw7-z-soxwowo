# DS5110
# Jitong Zou
# Mar 28, 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# ==== Step 1: Load dataset ====
df = pd.read_csv('./Data/Spotify_YouTube.csv')

# Select relevant features
X = df[['Liveness', 'Energy', 'Loudness']].copy()

# ==== Step 2: Standardize the data ====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ==== Step 3: Elbow Method to find optimal K ====
inertias = []
K_range = range(1, 15) # I choose from this range, but also can set other range like (1,10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=0)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

# ==== Step 4: Plot and save Elbow Graph ====
os.makedirs('./image', exist_ok=True)

plt.figure(figsize=(8, 5))
plt.plot(K_range, inertias, marker='o')
plt.title('Elbow Method to Determine Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (Within-Cluster Sum of Squares)')
plt.grid(True)
plt.tight_layout()
plt.savefig('./image/Elbow_Method.png')
plt.show()

print("Elbow plot saved to ./image/Elbow_Method.png")