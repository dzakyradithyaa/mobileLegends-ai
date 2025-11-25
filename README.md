# 🛡️ Mobile Legends Hero Classifier (MobileNetV2 Transfer Learning)

Proyek ini bertujuan untuk membangun model _Machine Learning_ berbasis _Transfer Learning_ menggunakan **MobileNetV2** untuk mengklasifikasikan 10 Hero Mobile Legends berdasarkan _in-game screenshot_.

## 🚀 Status Proyek

| Metrik                               | Nilai                          | Catatan                                                                   |
| :----------------------------------- | :----------------------------- | :------------------------------------------------------------------------ |
| **Arsitektur Dasar**                 | MobileNetV2 (ImageNet Weights) | Digunakan sebagai Feature Extractor.                                      |
| **Lapisan yang Dibuka (_Unfrozen_)** | 10 Lapisan Terakhir            | Agar model dapat belajar fitur spesifik Hero.                             |
| **Akurasi Validasi Tertinggi**       | $\mathbf{33.33\%}$             | **Hasil Konsisten Terbaik** (dengan LR 0.0002).                           |
| **Best-Case Akurasi**                | $\mathbf{45.83\%}$             | Pernah dicapai, namun sulit direplikasi karena _overfitting_.             |
| **Isu Utama**                        | _Overfitting_ Parah            | Akurasi Training $>85\%$, menunjukkan perlunya penambahan/perbaikan data. |

## 📁 Struktur Direktori

```
MobileLegends-apps/
├── backend/
│ ├── models/
│ │ ├── best_hero_classifier.h5 # Bobot model terbaik (Akurasi ~33.33%)
│ │ └── hero_labels.pkl         # Label kelas Hero yang tersimpan
│ ├── venv/                     # Virtual environment
│ ├── train_model.py            # Script utama untuk training model
│ ├── test_model.py             # Script untuk menguji model yang tersimpan
│ └── analyze_data.py           # Script untuk visualisasi data (t-SNE, Isomap)
└── dataset/
    ├── hero_a/
    ├── hero_b/
    └── ...
```

## ⚙️ Persyaratan Sistem

Pastikan Anda memiliki Python **3.8+** terinstal.

### Instalasi Lingkungan Virtual (Opsional, tapi Direkomendasikan)

```bash
python -m venv venv
# Aktifkan venv
# Di Windows (CMD/PowerShell):
.\venv\Scripts\activate
# Di Linux/macOS:
source venv/bin/activate
```

### Instalasi Dependensi

Instal semua _library_ yang diperlukan:

```bash
pip install tensorflow keras numpy scikit-learn matplotlib pandas
```

## 🎯 Instruksi Menjalankan (Training dan Analisis)

### 1\. Pelatihan Model (Jika Ingin Mencoba Mengulang)

_Script_ `train_model.py` dikonfigurasi untuk menjalankan $\mathbf{17}$ _Epoch_ dengan Learning Rate $\mathbf{0.0002}$ untuk mendapatkan akurasi terbaik secara konsisten. Bobot terbaik akan disimpan di `models/best_hero_classifier.h5`.

```bash
python train_model.py
```

> **Catatan:** Jangan menjalankan _training_ berulang kali jika Anda puas dengan hasil $33.33\%$ yang tersimpan saat ini, untuk menghindari risiko penimpaan bobot.

### 2\. Menguji Akurasi Model yang Tersimpan

Gunakan _script_ ini untuk memverifikasi akurasi model yang saat ini ada di `best_hero_classifier.h5`:

```bash
python test_model.py
```

### 3\. Analisis Kualitas Data (t-SNE, Isomap, LLE)

Gunakan _script_ ini untuk memvisualisasikan fitur yang diekstrak oleh MobileNetV2 dan melihat tingkat pemisahan Hero.

```bash
python analyze_data.py
```

Hasil visualisasi yang menunjukkan titik-titik (Hero) yang saling tumpang tindih mengkonfirmasi bahwa **peningkatan kualitas data (cropping) atau penambahan kuantitas data sangat diperlukan** untuk mencapai akurasi di atas $50\%$.

## 🧠 Konfigurasi Model Utama

Berikut adalah parameter kunci yang digunakan dalam _script_ `train_model.py`:

| Parameter             | Nilai                           | Tujuan                                                            |
| :-------------------- | :------------------------------ | :---------------------------------------------------------------- |
| **Model**             | MobileNetV2                     | Efisien dan cepat untuk _mobile_ atau _web_.                      |
| **Input Size**        | $128 \times 128$                | Ukuran gambar standar untuk efisiensi.                            |
| **Optimizer**         | Adam ($\mathbf{LR}=0.0002$)     | Learning Rate yang relatif rendah untuk stabilitas _fine-tuning_. |
| **Dropout**           | $0.6$                           | Regulasi tinggi untuk memerangi _overfitting_.                    |
| **Data Augmentation** | Rotation, Zoom, Horizontal Flip | Digunakan untuk menambah variasi data.                            |

## 🤝 Kontribusi

Selamat datang kontribusi dalam bentuk:

1.  **Penambahan Data:** Mengumpulkan lebih banyak gambar Hero (target $\ge 50$ gambar per Hero) dan memastikan gambar sudah di-_crop_ tanpa elemen UI game.
2.  **Eksperimen Model:** Mencoba arsitektur lain (misalnya ResNet50 atau VGG16) untuk perbandingan.
3.  **Integrasi:** Mengembangkan _API endpoint_ menggunakan **FastAPI** untuk _deployment_ model.
