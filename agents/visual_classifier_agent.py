# agents/visual_classifier_agent.py

import os
import time
from typing import List, Dict
from pdf2image import convert_from_path
from langgraph.state_schema import AgentState
from utils.visual_detection import detect_visual_regions, classify_visual_chunk
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

MEDIA_IMAGE_DIR = "media/page_images"
VISUAL_CHUNKS_DIR = "media/visual_chunks"
os.makedirs(MEDIA_IMAGE_DIR, exist_ok=True)
os.makedirs(VISUAL_CHUNKS_DIR, exist_ok=True)


def visual_classifier_agent(state: AgentState) -> AgentState:
    pdf_path = state.pdf_path
    pages = convert_from_path(pdf_path, dpi=150)
    visual_labels: List[Dict] = []

    print(f"📄 Processing {len(pages)} pages for visual classification...")

    for i, page_img in enumerate(pages):
        page_number = i + 1
        print(f"\n📃 Page {page_number} processing started...")
        page_start = time.time()

        page_path = os.path.join(MEDIA_IMAGE_DIR, f"page_{page_number}.png")
        page_img.save(page_path)

        # Detect candidate regions using OpenCV
        regions = detect_visual_regions(page_path)
        print(f"🔍 Detected {len(regions)} candidate visual blocks on page {page_number}")

        chunk_paths = []
        region_metadata = []

        for j, (x, y, w, h) in enumerate(regions):
            if w < 200 or h < 100:
                continue  # Skip small irrelevant blocks

            crop = page_img.crop((x, y, x + w, y + h))
            chunk_path = os.path.join(VISUAL_CHUNKS_DIR, f"page{page_number}_chunk{j}.png")
            crop.save(chunk_path)

            chunk_paths.append(chunk_path)
            region_metadata.append({"page": page_number, "bbox": (x, y, x + w, y + h)})

        # Run Gemini Vision in parallel
        def classify_chunk(i, chunk_path):
            start_time = time.time()
            visual_type, caption = classify_visual_chunk(chunk_path)
            elapsed = round(time.time() - start_time, 2)
            print(f"⏱️ Chunk {i+1}/{len(chunk_paths)} classified in {elapsed}s → {visual_type}")
            return visual_type, caption

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(classify_chunk, i, path) for i, path in enumerate(chunk_paths)]
            for i, future in enumerate(as_completed(futures)):
                visual_type, caption = future.result()
                meta = region_metadata[i]
                visual_labels.append({
                    "page": meta["page"],
                    "bbox": meta["bbox"],
                    "image_path": chunk_paths[i],
                    "visual_type": visual_type,
                    "caption": caption
                })

        print(f"✅ Page {page_number} completed in {round(time.time() - page_start, 2)}s")

    print(f"\n🧠 Total classified visual elements: {len(visual_labels)}")
    state.visual_labels = visual_labels
    return state