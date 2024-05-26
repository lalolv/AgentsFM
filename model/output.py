from pydantic import BaseModel, Field


class OutScript(BaseModel):
    title: str = Field(description="The Chinese title")
    content: str = Field(
        description="A coherent and amazing plain Chinese text, up to 3000 words")
