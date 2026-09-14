"""
Mock OCR service for local testing when tesseract is not installed.
This provides fake but realistic data for testing the application flow.
"""

def extract_text_with_confidence(image_path):
    """
    Mock OCR function that returns fake but realistic identity data.
    Use this when tesseract binary is not installed on the system.
    """
    
    # Return realistic mock data
    mock_text = """
    GOVERNMENT OF INDIA
    AADHAAR CARD
    
    Name: Rajesh Kumar Sharma
    Date of Birth: 15/08/1990
    Gender: Male
    Aadhaar Number: 1234 5678 9012
    
    Address: 123, MG Road
    Bangalore, Karnataka
    560001
    """
    
    # Mock confidence score (70-95% realistic range)
    mock_confidence = 85.5
    
    print(f"[MOCK OCR] Using mock data for: {image_path}")
    
    return mock_text.strip(), mock_confidence
