from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from services.ocr import extract_text_with_confidence
from services.data_extraction import extract_fields
from services.document_analysis import analyze_document
from services.tampering_detection import detect_tampering
from services.risk_engine import calculate_risk
from services.face_verification import verify_faces
from services.data_consistency import check_consistency

import shutil
import os


app = FastAPI(title="Fake Document Screening System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Fake Document Screening API is running!"
    }


@app.post("/ocr")
async def ocr_document(
    document_file: UploadFile = File(...),
    reference_file: UploadFile = File(...)
):
    document_path = f"temp_document_{document_file.filename}"
    reference_path = f"temp_reference_{reference_file.filename}"

    with open(document_path, "wb") as buffer:
        shutil.copyfileobj(document_file.file, buffer)

    with open(reference_path, "wb") as buffer:
        shutil.copyfileobj(reference_file.file, buffer)

    try:
        # OCR
        text, ocr_confidence = extract_text_with_confidence(
            document_path
        )

        # Structured fields
        fields = extract_fields(text)

        # Data consistency
        consistency = check_consistency(fields)

        # Image analysis
        analysis = analyze_document(document_path)

        # Tampering analysis
        tampering = detect_tampering(document_path)

        # Face verification
        face_result = verify_faces(
            document_path,
            reference_path
        )

        # Risk engine
        risk = calculate_risk(
            analysis,
            tampering,
            fields,
            face_result,
            consistency
        )

        return {
            "status": "success",
            "document_filename": document_file.filename,
            "reference_filename": reference_file.filename,

            "extracted_text": text,
            "ocr_confidence": ocr_confidence,

            "fields": fields,
            "data_consistency": consistency,

            "document_analysis": analysis,
            "tampering_analysis": tampering,
            "face_verification": face_result,

            "risk_assessment": risk
        }

    finally:
        if os.path.exists(document_path):
            os.remove(document_path)

        if os.path.exists(reference_path):
            os.remove(reference_path)