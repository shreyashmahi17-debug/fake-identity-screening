import re


def extract_fields(text):
    data = {
        "name": None,
        "date_of_birth": None,
        "gender": None,
        "document_number": None
    }

    # Clean OCR text
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # -------------------------
    # NAME
    # -------------------------

    name_match = re.search(
        r"(?:Name|NAme|NAME)\s*[:\-]?\s*([A-Za-z]+(?:\s+[A-Za-z]+){0,3})",
        text,
        re.IGNORECASE
    )

    if name_match:
        data["name"] = name_match.group(1).strip()

    # If "Name:" is not present, look for a likely person-name line
    if data["name"] is None:
        for line in lines:
            if re.fullmatch(
                r"[A-Za-z]+(?:\s+[A-Za-z]+){1,3}",
                line
            ):
                if line.lower() not in [
                    "government of india",
                    "aadhaar fake",
                    "patna bihar india"
                ]:
                    data["name"] = line
                    break

    # -------------------------
    # DATE OF BIRTH
    # -------------------------

    dob_match = re.search(
        r"(?:DOB|Date of Birth|Birth)\s*[:\-]?\s*"
        r"(\d{2}[-/]\d{2}[-/]\d{4})",
        text,
        re.IGNORECASE
    )

    if dob_match:
        data["date_of_birth"] = dob_match.group(1)

    # Also detect standalone date
    if data["date_of_birth"] is None:
        date_match = re.search(
            r"\b\d{2}[-/]\d{2}[-/]\d{4}\b",
            text
        )

        if date_match:
            data["date_of_birth"] = date_match.group(0)

    # -------------------------
    # GENDER
    # -------------------------

    gender_match = re.search(
        r"\b(Male|Female|Other)\b",
        text,
        re.IGNORECASE
    )

    if gender_match:
        data["gender"] = gender_match.group(1).capitalize()

    # -------------------------
    # DOCUMENT NUMBER
    # -------------------------

    number_match = re.search(
        r"\b\d{4}\s+\d{4}\s+\d{4}\b",
        text
    )

    if number_match:
        data["document_number"] = number_match.group(0)

    return data