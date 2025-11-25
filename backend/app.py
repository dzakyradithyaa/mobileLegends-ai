from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
import os

# --- KONFIGURASI API ---
app = FastAPI(title="Hero Classification API (Single Output)")

# 1. Konfigurasi CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- KONFIGURASI ML ---
MODEL_PATH = 'models/best_hero_classifier.h5'
IMG_SIZE = (128, 128)

# 2. DEFINISI LABEL
HERO_LABELS = [
    'Alucard', 'Layla', 'Gusion', 'Kagura', 'Miya',
    'Zilong', 'Lylia', 'Khufra', 'Estes', 'Claude'
]

# MAPPING HERO → ROLE
HERO_TO_ROLE = {
    'Alucard': 'Fighter',
    'Layla': 'Marksman',
    'Gusion': 'Assassin',
    'Kagura': 'Mage',
    'Miya': 'Marksman',
    'Zilong': 'Fighter',
    'Lylia': 'Mage',
    'Khufra': 'Tank',
    'Estes': 'Support',
    'Claude': 'Marksman'
}

# 3. Load Model
model_classifier = None
try:
    if os.path.exists(MODEL_PATH):
        model_classifier = load_model(MODEL_PATH)
        print("✅ Model Klasifikasi Output Tunggal Berhasil Dimuat.")
    else:
        print(f"❌ File model tidak ditemukan di: {MODEL_PATH}")
except Exception as e:
    print(f"❌ Gagal memuat model. Error: {e}")

# --- Fungsi Pembantu ---
def read_imagefile(file) -> Image.Image:
    return Image.open(BytesIO(file)).convert('RGB')

# --- Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Hero Classifier API is running!"}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if model_classifier is None:
        raise HTTPException(status_code=503, detail="Model belum dimuat.")

    try:
        contents = await file.read()
        img_pil = read_imagefile(contents)

        # Dummy bounding box full image
        bounding_box = [0, 0, img_pil.width, img_pil.height]

        # Resize image
        cropped = img_pil.crop((0, 0, img_pil.width, img_pil.height)).resize(IMG_SIZE)
        img_array = np.expand_dims(np.array(cropped) / 255.0, axis=0)

        # Prediksi
        predictions = model_classifier.predict(img_array)
        hero_probabilities = predictions[0]

        hero_name = HERO_LABELS[np.argmax(hero_probabilities)]
        hero_role = HERO_TO_ROLE.get(hero_name, "Unknown")
        hero_confidence_score = float(np.max(hero_probabilities))

        return JSONResponse(content={
            "filename": file.filename,
            "prediction": {
                "hero": hero_name,
                "role": hero_role,
                "bbox": bounding_box,
                "hero_confidence_score": hero_confidence_score,
                "role_confidence_score": 1.0  # Statis 100%
            }
        })

    except Exception as e:
        print(f"Error saat prediksi: {e}")
        raise HTTPException(status_code=500, detail="Terjadi error saat memproses gambar.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
