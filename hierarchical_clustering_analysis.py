# DS5110
# Jitong Zou
# Mar 28, 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from mpl_toolkits.mplot3d import Axes3D
import os

# === Step 1: Load and scale data ===
df = pd.read_csv('./Data/Spotify_YouTube.csv')
X = df[['Liveness', 'Energy', 'Loudness']].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Step 2: Dendrogram with cut line ===
Z = linkage(X_scaled, method='ward')

os.makedirs('./image', exist_ok=True)

plt.figure(figsize=(14, 6))
dendrogram(Z, truncate_mode='lastp', p=30, leaf_rotation=90, leaf_font_size=12, show_contracted=True)
plt.title('Hierarchical Clustering Dendrogram (Truncated)')
plt.xlabel('Clustered Samples')
plt.ylabel('Distance')

# Use horizontal line at y=90 for auto cut
cut_distance = 90
plt.axhline(y=cut_distance, color='red', linestyle='--', label=f'Cut at y={cut_distance}')
plt.legend()
plt.tight_layout()
plt.savefig('./image/Hierarchical_Dendrogram.png')
plt.show()

# === Step 3: Use fcluster to assign labels ===
labels_hc = fcluster(Z, t=cut_distance, criterion='distance')
n_clusters = len(np.unique(labels_hc))
df['HC_Cluster'] = labels_hc

print(f"Detected number of clusters: {n_clusters}")

# === Step 4: Cluster centers (original scale) ===
cluster_centers = df.groupby('HC_Cluster')[['Liveness', 'Energy', 'Loudness']].mean()
cluster_centers.index.name = 'Cluster'
print("Hierarchical Cluster Centers (Original Scale):")
print(cluster_centers)

# === Step 5: Define labels for 3 clusters ===
label_dict = {
    1: "Very Quiet, Low Energy",
    2: "Studio Style High Energy",
    3: "High Liveness, Loud (Live Feel)"
}
df['HC_Label'] = df['HC_Cluster'].map(label_dict)

# === Step 6: 3D visualization ===
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(
    X['Liveness'], X['Energy'], X['Loudness'],
    c=labels_hc,
    cmap='tab10',
    s=50,
    alpha=0.7
)

ax.set_title(f'Hierarchical Clustering of Spotify/YouTube Songs (n={n_clusters})', fontsize=14)
ax.set_xlabel('Liveness')
ax.set_ylabel('Energy')
ax.set_zlabel('Loudness')

# Legend using semantic labels
handles, _ = scatter.legend_elements(prop='colors')
legend_labels = [label_dict[i] for i in sorted(np.unique(labels_hc))]
ax.legend(handles, legend_labels, title="Clusters", bbox_to_anchor=(1.2, 1), loc='upper left')

plt.tight_layout()
plt.savefig('./image/Hierarchical_3D_Clusters.png')
plt.show()
