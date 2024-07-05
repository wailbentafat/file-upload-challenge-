from pydantic import BaseModel

class file(BaseModel):
    filename: str
    type: str
    size: int
