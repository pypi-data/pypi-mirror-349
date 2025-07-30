# Schema for Text-to-Image generation
from pydantic import BaseModel, Field

class Text2VideoInput(BaseModel):
    """Input model for text-to-video generation."""
    prompt: str = Field(
        ...,
        json_schema_extra={"x-sr-order": 200},
        max_length=2500,
        description='The prompt for the video'
    )
