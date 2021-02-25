from pydantic import BaseModel
from typing import Dict, List, Optional

class Image(BaseModel):
    caption: str
    when: str

class Comments(BaseModel):
    additional_comments: Optional[str]
    tags: List[str]
    img: Dict[str, Image]

class LocationBounds(BaseModel):
    maxLatitude: float
    minLatitude: float
    maxLongitude: float
    minLongitude: float

class UserReport(BaseModel):
    latitude: float
    longitude: float
    smell_value: int
    smell_description: Optional[str]
    feeling_symptoms: Optional[str]
    additional_comments: Optional[Comments]
    zip_code_id: Optional[int]
    observed_at: int
    zipcode: Optional[str]

