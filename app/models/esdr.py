from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    id: int
    name: str
    feedIds: List[int] = []

