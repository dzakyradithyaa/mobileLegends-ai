import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D

from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# ============================================================
# 1. KONFIGURASI
# ============================================================
DATASET_DIR = '../dataset/'
IMG_SIZE = (128, 128)
BATCH_SIZE = 16


# ============================================================
# 2. MUAT FEATURE EXTRACTOR DARI MobileNetV2
# ============================================================
print("Memuat MobileNetV2 sebagai feature extractor...")

try:
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(*IMG_SIZE, 3)
    )

    # Ambil output dari layer terakhir Conv block: 'Conv_1'
    x = base_model.get_layer('Conv_1').output

    # Tambahkan GlobalAveragePooling2D untuk meratakan fitur
    x = GlobalAveragePooling2D()(x)

    # Bentuk feature extractor baru
    feature_extractor = Model(inputs=base_model.input, outputs=x)

    print("✅ MobileNetV2 Feature Extractor siap.")

except Exception as e:
    print(f"❌ ERROR saat memuat MobileNetV2: {e}")
    exit()


# ============================================================
# 3. LOAD DATASET (TANPA AUGMENTASI)
# ============================================================
datagen = ImageDataGenerator(rescale=1.0 / 255)

data_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False   # Agar urutan label tidak berubah
)


# ============================================================
# 4. EKSTRAKSI FITUR + LABEL
# ============================================================
print("Mengekstrak fitur dari semua gambar...")

X_features = feature_extractor.predict(
    data_generator,
    steps=len(data_generator),
    verbose=1
)

y_labels = data_generator.classes
hero_names = list(data_generator.class_indices.keys())
y_names = [hero_names[i] for i in y_labels]

print(f"Bentuk fitur yang diekstrak (X): {X_features.shape}")


# ============================================================
# 5. FUNGSI PLOT REDUKSI DIMENSI
# ============================================================
def plot_reduction(X_2d, _, method_name):
    df = pd.DataFrame({
        'Dim1': X_2d[:, 0],
        'Dim2': X_2d[:, 1],
        'Hero': y_names
    })

    plt.figure(figsize=(12, 10))
    for hero, group in df.groupby('Hero'):
        plt.scatter(group['Dim1'], group['Dim2'], label=hero, alpha=0.7)

    plt.title(f'Visualisasi Fitur Hero MLBB: {method_name}', fontsize=16)
    plt.legend(title='Hero', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()


# ============================================================
# 6. REDUKSI DIMENSI
# ============================================================

# --- A. t-SNE ---
print("\n--- Menerapkan t-SNE (perplexity = 30) ---")
tsne = TSNE(
    n_components=2,
    random_state=42,
    perplexity=30,
    n_jobs=-1
)
X_tsne = tsne.fit_transform(X_features)
plot_reduction(X_tsne, 't-SNE', 't-SNE')


# --- B. Isomap ---
print("\n--- Menerapkan Isomap (neighbors = 10) ---")
iso = Isomap(
    n_components=2,
    n_neighbors=10,
    n_jobs=-1
)
X_iso = iso.fit_transform(X_features)
plot_reduction(X_iso, 'Isomap', 'Isomap')


# --- C. LLE ---
print("\n--- Menerapkan LLE (neighbors = 10) ---")
lle = LocallyLinearEmbedding(
    n_components=2,
    n_neighbors=10,
    method='standard',
    random_state=42,
    n_jobs=-1
)

try:
    X_lle = lle.fit_transform(X_features)
    plot_reduction(X_lle, 'LLE', 'Locally Linear Embedding (LLE)')
except ValueError as e:
    print(f"❗ WARNING: LLE gagal karena jumlah data terlalu sedikit atau struktur tidak cocok.\n{e}")


# ============================================================
# 7. SELESAI
# ============================================================
print("\n========================================================")
print("✅ Analisis Reduksi Dimensi Selesai.")
print("========================================================")
