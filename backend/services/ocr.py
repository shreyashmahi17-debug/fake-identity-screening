import pytesseract
import cv2
import sys
import os

# On Windows, point to the local Tesseract install.
# On Linux (Render / production), Tesseract is installed via apt and found automatically.
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


def extract_text_with_confidence(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return "", 0

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    processed = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    data = pytesseract.image_to_data(
        processed,
        output_type=pytesseract.Output.DICT
    )

    words = []
    confidences = []

    for text, conf in zip(data["text"], data["conf"]):

        text = text.strip()

        try:
            conf = float(conf)
        except ValueError:
            continue

        if text and conf >= 0:
            words.append(text)
            confidences.append(conf)

    extracted_text = "\n".join(words)

    if confidences:
        confidence = sum(confidences) / len(confidences)
    else:
        confidence = 0

    return extracted_text, round(confidence, 2)