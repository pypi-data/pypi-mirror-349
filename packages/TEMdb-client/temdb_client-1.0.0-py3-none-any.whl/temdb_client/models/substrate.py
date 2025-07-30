from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel, Field

class ReferencePoints(BaseModel):
    origin: Optional[Tuple[float, float, float]] = None
    end: Optional[Tuple[float, float, float]] = None
    ref: Optional[Tuple[float, float, float]] = None

    class Config:
        extra = 'allow'

class Aperture(BaseModel):
    uid: str = Field(...)
    index: int = Field(...)
    centroid: Optional[Tuple[float, float, float]] = None
    shape: Optional[str] = None
    shape_type: Optional[str] = None
    shape_params: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    tracking_uid: Optional[str] = Field(None, alias="tuid")

    class Config:
        extra = 'allow'
        validate_by_name = True 

class SubstrateMetadata(BaseModel):
    name: Optional[str] = None
    user: Optional[str] = None
    created: Optional[datetime] = None
    calibrated: Optional[datetime] = None
    extra: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = 'allow'

class SubstrateBase(BaseModel):
    media_type: Optional[str] = None
    uid: Optional[str] = None
    status: Optional[str] = None
    refpoint: Optional[ReferencePoints] = None
    refpoint_world: Optional[ReferencePoints] = None
    source_path: Optional[str] = None
    metadata: Optional[SubstrateMetadata] = None
    apertures: Optional[List[Aperture]] = None
    media_id: Optional[str] = None

    class Config:
        extra = 'allow'

class SubstrateCreate(SubstrateBase):
    media_id: str = Field(...)
    media_type: str = Field(...)
    status: Optional[str] = "new" 

class SubstrateUpdate(SubstrateBase):
    pass

class SubstrateResponse(SubstrateBase):
    media_id: str = Field(...)
    media_type: str = Field(...)
    created_at: datetime
    updated_at: Optional[datetime] = None
