# utils/visual_detection.py

import cv2
import numpy as np
from PIL import Image
from services.gemini_client import gemini_vision_chat

def detect_visual_regions(image_path, min_area=5000):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binarized = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binarized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if area >= min_area:
            regions.append((x, y, w, h))

    return regions

def classify_visual_chunk(image_path: str):
    prompt = """You are a document analyst. Analyze this image and classify it as one of the following:
- Table
- Chart
- Figure
- Diagram
- Text block
Then also extract a short caption if visible."""

    vision_response = gemini_vision_chat(prompt, image_path)

    visual_type = "unknown"
    caption = None

    if "table" in vision_response.lower():
        visual_type = "table"
    elif "chart" in vision_response.lower():
        visual_type = "chart"
    elif "figure" in vision_response.lower():
        visual_type = "figure"
    elif "diagram" in vision_response.lower():
        visual_type = "diagram"
    elif "text" in vision_response.lower():
        visual_type = "text block"

    # Extract first sentence or line as caption
    lines = vision_response.strip().splitlines()
    for line in lines:
        if line.strip() and not line.strip().lower().startswith("this is"):
            caption = line.strip()
            break

    return visual_type, caption
