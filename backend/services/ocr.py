import pytesseract
import cv2
import sys

# On Windows, point to the local Tesseract install.
# On Linux (Render / production), Tesseract is installed via apt and found automatically.
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

# Minimum Tesseract confidence (0-100) for a detected word to be trusted.
# Anything below this is treated as noise and dropped.
MIN_WORD_CONFIDENCE = 45


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

    # Group words back into their original lines using Tesseract's own
    # block/paragraph/line indices, instead of flattening every word
    # onto its own line. This keeps "Rohit Sharma" together as one line
    # the way it actually appears on the document.
    lines = {}
    confidences = []

    n = len(data["text"])
    for i in range(n):
        text = data["text"][i].strip()

        try:
            conf = float(data["conf"][i])
        except (ValueError, TypeError):
            continue

        # Drop low-confidence noise tokens (garbage OCR artifacts)
        if not text or conf < MIN_WORD_CONFIDENCE:
            continue

        line_key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
        lines.setdefault(line_key, []).append((data["left"][i], text))
        confidences.append(conf)

    # Sort words within each line left-to-right, then join lines in order
    extracted_lines = []
    for line_key in sorted(lines.keys()):
        words_in_line = sorted(lines[line_key], key=lambda w: w[0])
        extracted_lines.append(" ".join(w[1] for w in words_in_line))

    extracted_text = "\n".join(extracted_lines)

    confidence = round(sum(confidences) / len(confidences), 2) if confidences else 0

    return extracted_text, confidence