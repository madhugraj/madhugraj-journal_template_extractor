# agents/upload_agent.py
import os
import shutil
from langgraph.state_schema import AgentState

UPLOAD_DIR = "media/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_agent(file_path: str) -> AgentState:
    filename = os.path.basename(file_path)
    saved_path = os.path.join(UPLOAD_DIR, filename)
    shutil.copyfile(file_path, saved_path)

    print(f"📁 File uploaded to: {saved_path}")
    return AgentState(file_path=saved_path)
