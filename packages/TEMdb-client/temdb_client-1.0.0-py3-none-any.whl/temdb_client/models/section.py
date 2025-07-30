from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from .enum_schemas import SectionQuality


class SectioningRunParameters(BaseModel):
    cutting_speed_mms: Optional[float] = None
    retract_speed_mms: Optional[float] = None
    water_level_mm: Optional[float] = None
    wafer_set_level: Optional[float] = None
    tape_speed: Optional[float] = None
    new_tape_speed: Optional[float] = None
    tape_cycle: Optional[float] = None
    cut_cycle: Optional[float] = None
    phiset: Optional[float] = None
    phi_offset: Optional[float] = None
    time_phi: Optional[float] = None
    water_added: Optional[bool] = None
    other_metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class SectionMetrics(BaseModel):
    quality: Optional[SectionQuality] = None
    thickness_um: Optional[float] = None
    knife_quality: Optional[str] = None
    tissue_confidence_score: Optional[float] = None
    run_parameters: Optional[SectioningRunParameters] = None

    class Config:
        extra = "allow"


class SectionBase(BaseModel):
    section_number: Optional[int] = Field(None, gt=0)
    timestamp: Optional[datetime] = None  #
    optical_image: Optional[Dict[str, Any]] = None
    aperture_uid: Optional[str] = None
    aperture_index: Optional[int] = None
    barcode: Optional[str] = None
    section_metrics: Optional[SectionMetrics] = None
    cutting_session_id: Optional[str] = None
    media_id: Optional[str] = None
    block_id: Optional[str] = None
    specimen_id: Optional[str] = None
    section_id: Optional[str] = None

    class Config:
        extra = "allow"


class SectionCreate(SectionBase):
    cutting_session_id: str = Field(...)
    media_id: str = Field(...)
    section_number: int = Field(..., gt=0)
    timestamp: datetime = Field(...)


class SectionUpdate(SectionBase):
    pass


class SectionResponse(SectionBase):
    section_id: str = Field(...)
    section_number: int = Field(..., gt=0)
    timestamp: datetime
    cutting_session_id: str
    block_id: str
    specimen_id: str
    media_id: str

    created_at: datetime
    updated_at: Optional[datetime] = None
