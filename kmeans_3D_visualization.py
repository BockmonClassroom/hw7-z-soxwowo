# DS5110
# Jitong Zou
# Mar 28, 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# === Step 1: Load and preprocess data ===
df = pd.read_csv('./Data/Spotify_YouTube.csv')
X = df[['Liveness', 'Energy', 'Loudness']].copy()

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Step 2: Apply KMeans with K=4 ===
K = 4
kmeans = KMeans(n_clusters=K, init='k-means++', random_state=0)
labels = kmeans.fit_predict(X_scaled)

# Save cluster centers in original scale for interpretation
centers_scaled = kmeans.cluster_centers_
centers_original = scaler.inverse_transform(centers_scaled)

center_df = pd.DataFrame(
    centers_original,
    columns=['Liveness', 'Energy', 'Loudness']
)
center_df.index.name = 'Cluster'

# Print cluster centers
print("K-Means Cluster Centers (Original Scale):")
print(center_df)

# === Step 3: Assign labels back to the original dataframe ===
df['Cluster'] = labels

# Interpreted labels based on cluster centers
cluster_labels = {
    0: "Quiet, Moderate Energy",
    1: "High Liveness, Mod-High Energy",
    2: "Studio Style High Energy",
    3: "Very Quiet, Low Energy"
}
df['Cluster_Label'] = df['Cluster'].map(cluster_labels)

# === Step 4: 3D Plot of Clusters ===
from mpl_toolkits.mplot3d import Axes3D

os.makedirs('./image', exist_ok=True)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(
    X['Liveness'], X['Energy'], X['Loudness'],
    c=labels, cmap='Set1', s=50, alpha=0.6
)

# Label axes and add title
ax.set_title('K-Means Clustering of Spotify/YouTube Songs (K=4)', fontsize=14)
ax.set_xlabel('Liveness')
ax.set_ylabel('Energy')
ax.set_zlabel('Loudness')

# Create a legend using the semantic labels
handles, _ = scatter.legend_elements(prop='colors')
legend_labels = [cluster_labels[i] for i in sorted(cluster_labels)]
ax.legend(handles, legend_labels, title="Clusters", bbox_to_anchor=(1.2, 1), loc='upper left')

plt.tight_layout()
plt.savefig('./image/KMeans_3D_Clusters.png')
plt.show()

