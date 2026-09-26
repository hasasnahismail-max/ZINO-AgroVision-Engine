import os
import json
import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ZINO AgroVision API Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = "/workspaces/ZINO-AgroVision-Engine"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "ZINO AgroVision AI Engine",
        "version": "1.0.0"
    }

@app.post("/analyze")
async def analyze_leaf(file: UploadFile = File(...)):
    input_path = os.path.join(IMAGES_DIR, "input_current.jpg")
    output_path = os.path.join(IMAGES_DIR, "output_analyzed.jpg")
    
    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())
        
    binary_path = os.path.join(BASE_DIR, "build/zino_agro")
    
    try:
        res = subprocess.run([binary_path, input_path, output_path], capture_output=True, text=True, check=True)
        data = json.loads(res.stdout.strip())
        data["analyzed_image_url"] = "/images/output_analyzed.jpg"
        return data
    except subprocess.CalledProcessError as err:
        raise HTTPException(status_code=500, detail=f"C++ Engine Error: {err.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
