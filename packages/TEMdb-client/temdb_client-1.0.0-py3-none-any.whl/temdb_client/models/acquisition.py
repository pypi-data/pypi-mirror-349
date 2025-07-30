from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

from .enum_schemas import AcquisitionStatus


class StorageLocation(BaseModel):
    location_type: str
    base_path: str
    is_current: bool
    date_added: datetime
    metadata: Dict[str, Any]

    class Config:
        extra = "allow"


class StorageLocationCreate(BaseModel):
    location_type: str
    base_path: str
    metadata: Dict[str, Any]

    class Config:
        extra = "allow"


class LensCorrectionModel(BaseModel):
    id: int
    type: str
    class_name: str
    data_string: str

    class Config:
        extra = "allow"


class Calibration(BaseModel):
    pixel_size: float
    rotation_angle: float
    lens_model: Optional[LensCorrectionModel] = None
    aperture_centroid: Optional[List[float]] = None

    class Config:
        extra = "allow"


class HardwareParams(BaseModel):
    scope_id: str
    camera_model: str
    camera_serial: str
    camera_bit_depth: int
    media_type: str

    class Config:
        extra = "allow"


class AcquisitionParams(BaseModel):
    magnification: int
    spot_size: int
    exposure_time: int
    tile_size: List[int]
    tile_overlap: float
    saved_bit_depth: int

    class Config:
        extra = "allow"


class AcquisitionBase(BaseModel):
    hardware_settings: Optional[HardwareParams] = None
    acquisition_settings: Optional[AcquisitionParams] = None
    calibration_info: Optional[Calibration] = None
    status: Optional[AcquisitionStatus] = None
    tilt_angle: Optional[float] = None
    lens_correction: Optional[bool] = None
    end_time: Optional[datetime] = None
    storage_locations: Optional[List[StorageLocation]] = None
    montage_set_name: Optional[str] = None
    sub_region: Optional[Dict[str, int]] = None
    replaces_acquisition_id: Optional[int] = None
    montage_id: Optional[str] = None
    acquisition_id: Optional[str] = None
    roi_id: Optional[int] = None
    acquisition_task_id: Optional[str] = None
    specimen_id: Optional[str] = None

    class Config:
        extra = "allow"


class AcquisitionCreate(AcquisitionBase):
    montage_id: str = Field(...)
    acquisition_id: str = Field(...)
    roi_id: int = Field(...)
    acquisition_task_id: str = Field(...)
    hardware_settings: HardwareParams = Field(...)
    acquisition_settings: AcquisitionParams = Field(...)
    tilt_angle: float = Field(...)
    lens_correction: bool = Field(...)

    status: AcquisitionStatus = AcquisitionStatus.IMAGING


class AcquisitionUpdate(AcquisitionBase):
    calibration_info: Optional[Dict[str, Any]] = None


class AcquisitionResponse(AcquisitionBase):
    acquisition_id: str = Field(...)
    montage_id: str = Field(...)
    specimen_id: str = Field(...)
    roi_id: int = Field(...)
    acquisition_task_id: str = Field(...)
    hardware_settings: HardwareParams
    acquisition_settings: AcquisitionParams
    status: AcquisitionStatus
    start_time: datetime

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
