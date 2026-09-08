import cv2
import numpy as np
import os


def detect_tampering(image_path):
    image = cv2.imread(image_path)

    if image is None:
        return {
            "status": "error",
            "message": "Unable to read image"
        }

    # -----------------------------
    # 1. Basic image information
    # -----------------------------
    height, width = image.shape[:2]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # 2. ELA Analysis
    # -----------------------------
    temp_path = "temp_ela.jpg"

    cv2.imwrite(
        temp_path,
        image,
        [cv2.IMWRITE_JPEG_QUALITY, 90]
    )

    compressed = cv2.imread(temp_path)

    difference = cv2.absdiff(
        image,
        compressed
    )

    diff_gray = cv2.cvtColor(
        difference,
        cv2.COLOR_BGR2GRAY
    )

    ela_score = float(
        np.mean(diff_gray)
    )

    max_error = int(
        np.max(diff_gray)
    )

    if os.path.exists(temp_path):
        os.remove(temp_path)

    # -----------------------------
    # 3. Edge Analysis
    # -----------------------------
    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_ratio = (
        cv2.countNonZero(edges)
        / (width * height)
    )

    # -----------------------------
    # 4. Noise Analysis
    # -----------------------------
    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    noise = cv2.absdiff(
        gray,
        blurred
    )

    noise_score = float(
        np.mean(noise)
    )

    # -----------------------------
    # 5. Determine anomaly levels
    # -----------------------------
    ela_anomaly = "LOW"

    if ela_score > 10:
        ela_anomaly = "HIGH"
    elif ela_score > 5:
        ela_anomaly = "MEDIUM"

    noise_anomaly = "LOW"

    if noise_score > 15:
        noise_anomaly = "HIGH"
    elif noise_score > 8:
        noise_anomaly = "MEDIUM"

    edge_anomaly = "NORMAL"

    if edge_ratio > 0.20:
        edge_anomaly = "HIGH"
    elif edge_ratio > 0.10:
        edge_anomaly = "MEDIUM"

    # -----------------------------
    # 6. Calculate tampering risk
    # -----------------------------
    risk_score = 0

    if ela_anomaly == "HIGH":
        risk_score += 50
    elif ela_anomaly == "MEDIUM":
        risk_score += 25

    if noise_anomaly == "HIGH":
        risk_score += 30
    elif noise_anomaly == "MEDIUM":
        risk_score += 15

    if edge_anomaly == "HIGH":
        risk_score += 20
    elif edge_anomaly == "MEDIUM":
        risk_score += 10

    risk_score = min(
        risk_score,
        100
    )

    # -----------------------------
    # 7. Final tampering level
    # -----------------------------
    if risk_score >= 60:
        tampering_risk = "HIGH"

    elif risk_score >= 30:
        tampering_risk = "MEDIUM"

    else:
        tampering_risk = "LOW"

    # -----------------------------
    # 8. Explainable reasons
    # -----------------------------
    reasons = []

    if ela_anomaly == "HIGH":
        reasons.append(
            "High compression inconsistency detected"
        )
    elif ela_anomaly == "MEDIUM":
        reasons.append(
            "Moderate compression inconsistency detected"
        )

    if noise_anomaly == "HIGH":
        reasons.append(
            "Unusual image noise pattern detected"
        )
    elif noise_anomaly == "MEDIUM":
        reasons.append(
            "Moderate noise variation detected"
        )

    if edge_anomaly == "HIGH":
        reasons.append(
            "High edge density detected"
        )
    elif edge_anomaly == "MEDIUM":
        reasons.append(
            "Moderate edge density detected"
        )

    if not reasons:
        reasons.append(
            "No major image-level anomaly detected"
        )

    return {
        "status": "success",

        "tampering_risk": tampering_risk,

        "tampering_score": risk_score,

        "ela_score": round(
            ela_score,
            2
        ),

        "max_error": max_error,

        "edge_ratio": round(
            edge_ratio,
            4
        ),

        "noise_score": round(
            noise_score,
            2
        ),

        "analysis": {
            "ela": ela_anomaly,
            "edge": edge_anomaly,
            "noise": noise_anomaly
        },

        "reasons": reasons
    }