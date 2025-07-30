from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from .enum_schemas import AcquisitionTaskStatus


class AcquisitionTaskBase(BaseModel):
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    task_type: Optional[str] = None
    status: Optional[AcquisitionTaskStatus] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    specimen_id: Optional[str] = None
    block_id: Optional[str] = None
    roi_id: Optional[int] = None
    task_id: Optional[str] = None
    version: Optional[int] = None

    class Config:
        extra = "allow"


class AcquisitionTaskCreate(AcquisitionTaskBase):
    task_id: str = Field(...)
    specimen_id: str = Field(...)
    block_id: str = Field(...)
    roi_id: int = Field(...)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    task_type: str = "standard_acquisition"
    version: int = 1
    status: AcquisitionTaskStatus = AcquisitionTaskStatus.PLANNED


class AcquisitionTaskUpdate(AcquisitionTaskBase):
    pass


class AcquisitionTaskResponse(AcquisitionTaskBase):

    task_id: str = Field(...)
    specimen_id: str = Field(...)
    block_id: str = Field(...)
    roi_id: int
    task_type: str
    version: int
    status: AcquisitionTaskStatus
    created_at: datetime

    updated_at: Optional[datetime] = None

