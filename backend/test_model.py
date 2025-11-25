import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import os

# --- KONFIGURASI ---
DATASET_DIR = '../dataset/'
IMG_SIZE = (128, 128)
BATCH_SIZE = 16
MODEL_PATH = 'models/best_hero_classifier.h5'

# --- 1. MEMPERSIAPKAN DATA VALIDASI ---
# Konfigurasi harus sama persis dengan saat training!
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2 
)

# Gunakan subset='validation' untuk memuat data validasi
val_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False # Matikan shuffle untuk evaluasi yang konsisten
)

# --- 2. LOAD MODEL TERBAIK ---
print("\n--- Menguji Model Tersimpan ---")
try:
    model_best = load_model(MODEL_PATH)
    print(f"✅ Model dari '{MODEL_PATH}' berhasil dimuat.")
except Exception as e:
    print(f"❌ Gagal memuat model. Pastikan file ada. Error: {e}")
    exit()

# --- 3. EVALUASI MODEL ---
# Langkah validasi per epoch harus sama seperti saat training
steps = val_generator.samples // BATCH_SIZE 
if steps == 0:
    steps = 1 

loss, acc = model_best.evaluate(
    val_generator, 
    steps=steps, 
    verbose=1
)

print("\n========================================================")
print(f"Hasil Evaluasi Model Terbaik yang Tersimpan:")
print(f"  Akurasi Validasi: {acc*100:.2f}%")
print(f"  Loss Validasi: {loss:.4f}")
print("========================================================")