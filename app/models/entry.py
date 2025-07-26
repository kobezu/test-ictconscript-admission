from pydantic import BaseModel, Field

class Entry(BaseModel):
  title: str = Field(max_length=120)
  body: str
  lat: float | None = None
  lon: float | None = None
