from pydantic import BaseModel
from typing import Dict, List, Optional

class Location(BaseModel):
    id: Optional[int]
    name: str
    regionId: Optional[int]
    regionName: Optional[str]
    feedIds: List[int]

class LocationItems(BaseModel):
    Succeeded: List[Location]
    Failed: List[Location]
    
class ChannelData(BaseModel):
    minTimeSecs: float
    maxTimeSecs: float
    minValue: float
    maxValue: float

class ChannelBounds(BaseModel):
    channels: Dict[str, ChannelData]
    minTimeSecs: float
    maxTimeSecs: float

class FeedData(BaseModel):
    id: int
    name: str
    deviceId: int
    productId: int
    userId: int
    apiKeyReadOnly: str
    exposure: str
    isPublic: bool
    isMobile: bool
    latitude: float
    longitude: float
    channelSpecs: dict
    channelBounds: ChannelBounds
    created: str
    modified: str
    lastUpload: str
    minTimeSecs: float
    maxtimeSecs: float

class Region(BaseModel):
    id: Optional[int]
    name: str
    locationIds: Optional[List[int]]
    
class RegionItems(BaseModel):
    Succeeded: List[Region]
    Failed: List[Region]
    
