# agents/layout_extractor_agent.py

import fitz  # PyMuPDF
from langgraph.state_schema import AgentState
import os
import json

def extract_layout_metadata(state: AgentState) -> AgentState:
    pdf_path = state.pdf_path
    doc = fitz.open(pdf_path)
    layout_info = []

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    font_size = span["size"]
                    bbox = span["bbox"]

                    if not text or font_size < 5:
                        continue
                    if bbox[2] - bbox[0] < 2 or bbox[3] - bbox[1] < 2:
                        continue

                    entry = {
                        "page": page_number,
                        "text": text,
                        "font": span["font"],
                        "size": round(font_size, 1),
                        "bbox": bbox,
                        "color": span["color"],
                        "flags": span["flags"],
                    }
                    layout_info.append(entry)

    # Dump to file
    os.makedirs("output/reports", exist_ok=True)
    with open("output/reports/layout_entries.json", "w", encoding="utf-8") as f:
        json.dump(layout_info, f, indent=2, ensure_ascii=False)
        print("📝 Full layout written to: output/reports/layout_entries.json")

    print(f"📐 Cleaned layout: {len(layout_info)} valid entries")
    state.layout_metadata = {
        "font_stats": summarize_fonts(layout_info),
        "elements": layout_info
    }
    return state

def summarize_fonts(entries):
    font_sizes = {}
    for entry in entries:
        size = entry["size"]
        font_sizes[size] = font_sizes.get(size, 0) + 1

    sorted_stats = sorted(font_sizes.items(), key=lambda x: x[1], reverse=True)
    return [{"size": size, "count": count} for size, count in sorted_stats]
