import re


def check_consistency(fields):
    issues = []
    checks = {
        "name": "PASS",
        "date_of_birth": "PASS",
        "gender": "PASS",
        "document_number": "PASS"
    }

    # -------------------------
    # NAME VALIDATION
    # -------------------------
    name = fields.get("name")

    if not name:
        checks["name"] = "MISSING"
        issues.append("Name is missing")

    elif len(name.strip()) < 3:
        checks["name"] = "INVALID"
        issues.append("Name appears too short")

    elif not re.fullmatch(
        r"[A-Za-z]+(?:\s+[A-Za-z]+){0,3}",
        name.strip()
    ):
        checks["name"] = "REVIEW"
        issues.append("Name contains unusual characters")

    # -------------------------
    # DATE OF BIRTH VALIDATION
    # -------------------------
    dob = fields.get("date_of_birth")

    if not dob:
        checks["date_of_birth"] = "MISSING"
        issues.append("Date of birth is missing")

    elif not re.fullmatch(
        r"\d{2}[-/]\d{2}[-/]\d{4}",
        dob
    ):
        checks["date_of_birth"] = "INVALID"
        issues.append("Date of birth format is invalid")

    else:
        day, month, year = map(
            int,
            re.split(r"[-/]", dob)
        )

        if month < 1 or month > 12:
            checks["date_of_birth"] = "INVALID"
            issues.append("Date of birth has invalid month")

        elif day < 1 or day > 31:
            checks["date_of_birth"] = "INVALID"
            issues.append("Date of birth has invalid day")

    # -------------------------
    # GENDER VALIDATION
    # -------------------------
    gender = fields.get("gender")

    if not gender:
        checks["gender"] = "MISSING"
        issues.append("Gender is missing")

    elif gender.lower() not in [
        "male",
        "female",
        "other"
    ]:
        checks["gender"] = "INVALID"
        issues.append("Gender value is invalid")

    # -------------------------
    # DOCUMENT NUMBER VALIDATION
    # -------------------------
    document_number = fields.get("document_number")

    if not document_number:
        checks["document_number"] = "MISSING"
        issues.append("Document number is missing")

    elif not re.fullmatch(
        r"\d{4}\s+\d{4}\s+\d{4}",
        document_number.strip()
    ):
        checks["document_number"] = "REVIEW"
        issues.append(
            "Document number format appears suspicious"
        )

    # -------------------------
    # FINAL STATUS
    # -------------------------
    invalid_count = sum(
        1
        for value in checks.values()
        if value == "INVALID"
    )

    missing_count = sum(
        1
        for value in checks.values()
        if value == "MISSING"
    )

    review_count = sum(
        1
        for value in checks.values()
        if value == "REVIEW"
    )

    total_issues = (
        invalid_count
        + missing_count
        + review_count
    )

    if invalid_count > 0:
        status = "FAIL"

    elif total_issues >= 3:
        status = "FAIL"

    elif total_issues > 0:
        status = "REVIEW"

    else:
        status = "PASS"

    return {
        "status": status,
        "issues": issues,
        "field_checks": checks,
        "summary": {
            "total_fields": 4,
            "valid_fields": 4 - total_issues,
            "issues_found": total_issues
        }
    }