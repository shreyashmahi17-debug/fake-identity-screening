import cv2


def analyze_document(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return {
            "status": "error",
            "message": "Unable to read image"
        }

    # Image dimensions
    height, width = image.shape[:2]

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur detection using Laplacian variance
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Brightness
    brightness = gray.mean()

    # Edge detection
    edges = cv2.Canny(gray, 100, 200)
    edge_pixels = cv2.countNonZero(edges)

    total_pixels = height * width
    edge_ratio = edge_pixels / total_pixels

    return {
        "image_width": width,
        "image_height": height,
        "blur_score": round(float(blur_score), 2),
        "brightness": round(float(brightness), 2),
        "edge_ratio": round(float(edge_ratio), 4)
    }