from pydantic import BaseModel, Field
from typing import Dict, Any

class EntityParser(BaseModel):
    output: Dict[str, Any] = Field(
        description="""
        
        """
    )

class DecisionParser(BaseModel):
    output: str = Field(
        description="""
        
        """
    )

class MemoryParser(BaseModel):
    output: Dict[str, Any] = Field(
        description="""

            """
    )