def detect_document_type(text):
    text_lower = text.lower()

    aadhaar_keywords = [
        "aadhaar",
        "government of india",
        "unique identification",
        "uidai"
    ]

    matches = sum(
        1 for keyword in aadhaar_keywords
        if keyword in text_lower
    )

    if matches >= 2:
        return {
            "document_type": "AADHAAR",
            "confidence": 90
        }

    return {
        "document_type": "UNKNOWN",
        "confidence": 0
    }