from pydantic import BaseModel, Field
from typing import List

class ChatbotResponse(BaseModel):
    category: str = Field(description="The detected category: Programming, Math, or General")
    main_answer: str = Field(description="Detailed response or answer to the user query")
    summary: str = Field(description="A brief 1-2 sentence summary of the main answer")
    keywords: List[str] = Field(description="List of key concepts or terms extracted from the response")