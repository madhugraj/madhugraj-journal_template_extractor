# langgraph/state_schema.py
from typing import Optional, Dict, List
from pydantic import BaseModel

class AgentState(BaseModel):
    file_path: str
    pdf_path: Optional[str] = None
    layout_metadata: Optional[Dict] = None
    visual_labels: Optional[List[Dict]] = None
    structure_summary: Optional[str] = None
    final_template: Optional[str] = None
