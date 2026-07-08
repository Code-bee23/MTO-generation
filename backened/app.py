from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import shutil
import os
import traceback

from ocr import extract_text
from ai import extract_components
from mto import generate_mto
from excel import create_excel

app = FastAPI(
    title="AI MTO Generator",
    description="Generate Material Take-Off from Isometric Drawings",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI MTO Generator Backend Running"
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    print("\n==============================")
    print("NEW FILE RECEIVED")
    print("==============================")

    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        return {
            "status": "error",
            "message": "Only PDF, PNG, JPG and JPEG are supported."
        }

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("File Saved :", file_path)

    try:

        # ---------------------------------
        # OCR
        # ---------------------------------

        print("\nRunning OCR...")

        ocr_text, image_path = extract_text(file_path)

        print("OCR Completed")
        print("--------------------------------")
        print(ocr_text)
        print("--------------------------------")

        # ---------------------------------
        # AI
        # ---------------------------------

        print("\nRunning LLaVA...")

        ai_data = extract_components(
            ocr_text,
            image_path
        )

        print("AI Extraction Completed")
        print(ai_data)

        # ---------------------------------
        # Generate MTO
        # ---------------------------------

        print("\nGenerating MTO...")

        mto = generate_mto(ai_data)

        print("MTO Generated")
        print(mto)

        # ---------------------------------
        # Excel
        # ---------------------------------

        excel_path = os.path.join(
            OUTPUT_FOLDER,
            "MTO.xlsx"
        )

        print("\nCreating Excel...")

        create_excel(
            mto_data=mto,
            ai_data=ai_data,
            output_file=excel_path
        )

        print("Excel Created :", excel_path)

        # ---------------------------------
        # Final Response
        # ---------------------------------

        response = {
            "status": "success",
            "filename": file.filename,
            "ocr_text": ocr_text,
            "ai_data": ai_data,
            "mto": mto,
            "excel": "MTO.xlsx"
        }

        print("\nSending Response to Frontend...")
        print(response)

        return response

    except Exception as e:

        print("\n========== ERROR ==========")
        traceback.print_exc()

        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/download")
def download_excel():

    excel_path = os.path.join(
        OUTPUT_FOLDER,
        "MTO.xlsx"
    )

    if not os.path.exists(excel_path):
        return {
            "status": "error",
            "message": "Excel file not found."
        }

    return FileResponse(
        excel_path,
        filename="MTO.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )