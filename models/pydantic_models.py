from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InputTexts(BaseModel):
    texts: List[str]

class InputTe(BaseModel):
    input_text: str
    sim_texts: List[str]
