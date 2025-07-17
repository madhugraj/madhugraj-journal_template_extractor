# test_runner.py
from agents.upload_agent import upload_agent
from agents.pdf_converter_agent import convert_to_pdf
from agents.layout_extractor_agent import extract_layout_metadata
from agents.visual_classifier_agent import visual_classifier_agent

# Simulate user input
INPUT_FILE = "data/7263-Royalcare Expansion Phase 3_Stage 1_TEV_DR_10Mar23_Fin.doc"  # Replace with your sample file path

# Run upload and conversion
state = upload_agent(INPUT_FILE)
state = convert_to_pdf(state)
state = extract_layout_metadata(state)
state = visual_classifier_agent(state)
