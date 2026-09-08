import cv2
import numpy as np


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def get_face_data(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    if len(faces) == 0:
        return None

    # Select the largest detected face
    x, y, w, h = max(
        faces,
        key=lambda face: face[2] * face[3]
    )

    face = gray[y:y + h, x:x + w]

    face = cv2.resize(
        face,
        (200, 200)
    )

    face = cv2.normalize(
        face,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return {
        "face": face,
        "box": {
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        },
        "image_width": int(image.shape[1]),
        "image_height": int(image.shape[0])
    }


def verify_faces(document_image, reference_image):

    document_data = get_face_data(document_image)
    reference_data = get_face_data(reference_image)

    # Document face not found
    if document_data is None:
        return {
            "status": "error",
            "message": "No face detected in document image"
        }

    # Reference face not found
    if reference_data is None:
        return {
            "status": "error",
            "message": "No face detected in reference image"
        }

    document_face = document_data["face"]
    reference_face = reference_data["face"]

    document_float = document_face.astype(np.float32)
    reference_float = reference_face.astype(np.float32)

    # Calculate image correlation
    correlation = cv2.matchTemplate(
        document_float,
        reference_float,
        cv2.TM_CCOEFF_NORMED
    )[0][0]

    correlation = float(
        max(-1.0, min(1.0, correlation))
    )

    # Convert correlation into a 0–100 prototype similarity score
    similarity_score = (
        (correlation + 1) / 2
    ) * 100

    similarity_score = round(
        similarity_score,
        2
    )

    # Prototype thresholds
    if correlation >= 0.70:
        verification = "MATCH"
        confidence = "HIGH"

    elif correlation >= 0.45:
        verification = "REVIEW"
        confidence = "MEDIUM"

    else:
        verification = "MISMATCH"
        confidence = "LOW"

    return {
        "status": "success",

        "similarity_score": similarity_score,

        "verification": verification,

        "confidence": confidence,

        "correlation": round(
            correlation,
            4
        ),

        "document_face_box": document_data["box"],

        "reference_face_box": reference_data["box"],

        "document_image_size": {
            "width": document_data["image_width"],
            "height": document_data["image_height"]
        },

        "reference_image_size": {
            "width": reference_data["image_width"],
            "height": reference_data["image_height"]
        }
    }