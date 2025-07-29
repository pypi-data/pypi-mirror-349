from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from yolov5 import YOLOv5
from PIL import Image, ImageDraw
import torch
import os
import io
import requests
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = "cuda" if torch.cuda.is_available() else "cpu"

# Model URLs (REPLACE with your actual URLs)
PERSON_MODEL_URL = "https://bhargo-test.s3.us-east-1.amazonaws.com/yolov5m.pt"
PAMPHLET_MODEL_URL = "https://bhargo-test.s3.us-east-1.amazonaws.com/last.pt"

# Cache directory
MODEL_DIR = os.path.join(Path.home(), ".pamphlet_detector_models")
os.makedirs(MODEL_DIR, exist_ok=True)

def download_model_if_needed(url: str, save_path: str):
    if not os.path.exists(save_path):
        print(f"Downloading models...")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        # print("Model downloaded to:", save_path)

# Download and load models
person_model_path = os.path.join(MODEL_DIR, "yolov5m.pt")
pamphlet_model_path = os.path.join(MODEL_DIR, "best.pt")

download_model_if_needed(PERSON_MODEL_URL, person_model_path)
download_model_if_needed(PAMPHLET_MODEL_URL, pamphlet_model_path)

person_model = YOLOv5(person_model_path, device=device)
pamphlet_model = YOLOv5(pamphlet_model_path, device=device)

# Overlap logic
def is_significant_overlap(person_box, pamphlet_box, overlap_thresh=0.5):
    xA = max(person_box[0], pamphlet_box[0])
    yA = max(person_box[1], pamphlet_box[1])
    xB = min(person_box[2], pamphlet_box[2])
    yB = min(person_box[3], pamphlet_box[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    personArea = (person_box[2] - person_box[0]) * (person_box[3] - person_box[1])

    return personArea > 0 and (interArea / personArea) > overlap_thresh

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        draw = ImageDraw.Draw(image)

        # Predict
        person_preds = person_model.predict(image)
        pamphlet_preds = pamphlet_model.predict(image)

        person_df = person_preds.pandas().xyxy[0]
        pamphlet_df = pamphlet_preds.pandas().xyxy[0]

        person_df = person_df[person_df['class'] == 0].copy()
        pamphlet_df = pamphlet_df[pamphlet_df['class'] == 0].copy()

        filtered_persons = []
        for _, person in person_df.iterrows():
            person_box = [person['xmin'], person['ymin'], person['xmax'], person['ymax']]
            overlapping = any(
                is_significant_overlap(person_box, [p['xmin'], p['ymin'], p['xmax'], p['ymax']])
                for _, p in pamphlet_df.iterrows()
            )
            if not overlapping:
                filtered_persons.append(person)

        return JSONResponse({
            "persons_detected": len(filtered_persons),
            "pamphlets_detected": len(pamphlet_df),
            "status": 200
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
