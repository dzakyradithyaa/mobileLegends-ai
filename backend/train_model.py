import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import numpy as np
import os
import pickle

# ============================================================
# 1. KONFIGURASI PROYEK
# ============================================================
DATASET_DIR = '../dataset/'
IMG_SIZE = (128, 128)
BATCH_SIZE = 16
EPOCHS = 17   # Batas ideal sesuai peak performa
MODEL_CHECKPOINT_PATH = 'models/best_hero_classifier.h5'

os.makedirs('models', exist_ok=True)

# ============================================================
# 2. DATA LOADING & GENERATOR
# ============================================================
print("Mempersiapkan data...")

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    rotation_range=15,
    zoom_range=0.15,
    horizontal_flip=True
)

train_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

HERO_LABELS = list(train_generator.class_indices.keys())
NUM_HEROES = len(HERO_LABELS)

print(f"Ditemukan {NUM_HEROES} Hero.")

# ============================================================
# 3. ARSITEKTUR MODEL (MobileNetV2)
# ============================================================
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)

# Unfreeze 10 layer terakhir
for layer in base_model.layers[-10:]:
    layer.trainable = True

# Custom head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.6)(x)

hero_output = Dense(NUM_HEROES, activation='softmax', name='hero_output')(x)

model = Model(inputs=base_model.input, outputs=hero_output)

# ============================================================
# 4. KOMPILASI MODEL
# ============================================================
model.compile(
    optimizer=Adam(learning_rate=0.0002),   # LR 0.0002 
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ============================================================
# 5. PELATIHAN MODEL (Tanpa Early Stopper)
# ============================================================
print("\n--- MULAI PELATIHAN MODEL (LR 0.0002, EPOCHS 17, TANPA EARLY STOP) ---")

checkpoint = ModelCheckpoint(
    MODEL_CHECKPOINT_PATH,
    monitor='val_accuracy',
    verbose=1,
    save_best_only=True,
    mode='max'
)

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_data=val_generator,
    validation_steps=val_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=[checkpoint]
)

# ============================================================
# 6. PENYIMPANAN LABEL HERO
# ============================================================
try:
    with open('models/hero_labels.pkl', 'wb') as f:
        pickle.dump(HERO_LABELS, f)
except Exception as e:
    print(f"❗ ERROR: Gagal menyimpan file .pkl: {e}")

print("\n========================================================")
print(f"✅ Pelatihan Selesai. Model terbaik tersimpan di: {MODEL_CHECKPOINT_PATH}")
print("========================================================")
