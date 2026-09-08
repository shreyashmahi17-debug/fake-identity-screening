def calculate_risk(
    document_analysis,
    tampering_analysis,
    fields,
    face_result,
    consistency
):
    breakdown = {
        "image_quality": 0,
        "tampering_detection": 0,
        "field_validation": 0,
        "face_verification": 0,
        "data_consistency": 0
    }

    reasons = []

    # =========================================
    # 1. IMAGE QUALITY
    # Maximum: 10
    # =========================================

    blur_score = document_analysis.get(
        "blur_score",
        0
    )

    brightness = document_analysis.get(
        "brightness",
        0
    )

    if blur_score < 50:
        breakdown["image_quality"] += 7
        reasons.append(
            "Image appears blurry"
        )

    elif blur_score < 100:
        breakdown["image_quality"] += 4
        reasons.append(
            "Image quality is slightly low"
        )

    if brightness < 40 or brightness > 220:
        breakdown["image_quality"] += 3
        reasons.append(
            "Unusual image brightness detected"
        )

    breakdown["image_quality"] = min(
        breakdown["image_quality"],
        10
    )

    # =========================================
    # 2. TAMPERING DETECTION
    # Maximum: 30
    # =========================================

    tampering_score = tampering_analysis.get(
        "tampering_score",
        0
    )

    tampering_risk = tampering_analysis.get(
        "tampering_risk",
        "LOW"
    )

    if tampering_risk == "HIGH":

        breakdown["tampering_detection"] = 30

        reasons.append(
            "High image-level tampering risk detected"
        )

    elif tampering_risk == "MEDIUM":

        breakdown["tampering_detection"] = 15

        reasons.append(
            "Moderate image-level anomaly detected"
        )

    else:

        breakdown["tampering_detection"] = 0

    # =========================================
    # 3. FIELD VALIDATION
    # Maximum: 20
    # =========================================

    required_fields = [
        "name",
        "date_of_birth",
        "gender",
        "document_number"
    ]

    missing_fields = [
        field
        for field in required_fields
        if not fields.get(field)
    ]

    if missing_fields:

        breakdown["field_validation"] = min(
            len(missing_fields) * 5,
            20
        )

        readable_fields = ", ".join(
            field.replace("_", " ")
            for field in missing_fields
        )

        reasons.append(
            "Missing or unclear fields: "
            + readable_fields
        )

    # =========================================
    # 4. FACE VERIFICATION
    # Maximum: 30
    # =========================================

    face_status = face_result.get(
        "status"
    )

    if face_status == "success":

        verification = face_result.get(
            "verification"
        )

        if verification == "MISMATCH":

            breakdown["face_verification"] = 30

            reasons.append(
                "Face does not match reference image"
            )

        elif verification == "REVIEW":

            breakdown["face_verification"] = 15

            reasons.append(
                "Face similarity requires manual review"
            )

        elif verification == "MATCH":

            breakdown["face_verification"] = 0

        else:

            breakdown["face_verification"] = 15

            reasons.append(
                "Face verification is inconclusive"
            )

    else:

        breakdown["face_verification"] = 30

        reasons.append(
            "Face verification failed"
        )

    # =========================================
    # 5. DATA CONSISTENCY
    # Maximum: 10
    # =========================================

    consistency_status = consistency.get(
        "status"
    )

    if consistency_status == "FAIL":

        breakdown["data_consistency"] = 10

        reasons.append(
            "Data consistency check failed"
        )

    elif consistency_status == "REVIEW":

        breakdown["data_consistency"] = 5

        reasons.append(
            "Data consistency requires review"
        )

    # =========================================
    # FINAL RISK SCORE
    # =========================================

    score = sum(
        breakdown.values()
    )

    score = min(
        score,
        100
    )

    # =========================================
    # RISK LEVEL
    # =========================================

    if score >= 70:

        risk_level = "HIGH"

        recommendation = (
            "Manual verification required"
        )

    elif score >= 40:

        risk_level = "MEDIUM"

        recommendation = (
            "Further verification recommended"
        )

    else:

        risk_level = "LOW"

        recommendation = (
            "No major anomaly detected"
        )

    # =========================================
    # CLEAN RESULT
    # =========================================

    return {

        "risk_score": score,

        "risk_level": risk_level,

        "risk_breakdown": breakdown,

        "risk_weights": {

            "image_quality": "10%",

            "tampering_detection": "30%",

            "field_validation": "20%",

            "face_verification": "30%",

            "data_consistency": "10%"
        },

        "reasons": reasons,

        "recommendation": recommendation
    }