from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from services.ocr import extract_text_with_confidence
from services.document_classifier import detect_document_type
from services.data_extraction import extract_fields
from services.document_analysis import analyze_document
from services.tampering_detection import detect_tampering
from services.risk_engine import calculate_risk
from services.face_verification import verify_faces
from services.data_consistency import check_consistency

import shutil
import os
import uuid

app = FastAPI(title="Fake Document Screening System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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
    # Use only the file extension from the uploaded name (never the raw
    # filename) and prefix with a per-request UUID. This avoids two
    # concurrent uploads overwriting each other's temp file, and avoids
    # writing to an attacker-controlled path (path traversal) if the
    # filename contains "../" or similar.
    document_ext = os.path.splitext(
        os.path.basename(document_file.filename or "")
    )[1]
    reference_ext = os.path.splitext(
        os.path.basename(reference_file.filename or "")
    )[1]

    request_id = uuid.uuid4().hex

    document_path = f"temp_document_{request_id}{document_ext}"
    reference_path = f"temp_reference_{request_id}{reference_ext}"

    with open(document_path, "wb") as buffer:
        shutil.copyfileobj(document_file.file, buffer)

    with open(reference_path, "wb") as buffer:
        shutil.copyfileobj(reference_file.file, buffer)

    try:
        # OCR
        text, ocr_confidence = extract_text_with_confidence(
            document_path
        )

        document_type = detect_document_type(text)

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

            "risk_assessment": risk,
            "document_type": document_type,
        }

    finally:
        if os.path.exists(document_path):
            os.remove(document_path)

        if os.path.exists(reference_path):
            os.remove(reference_path)