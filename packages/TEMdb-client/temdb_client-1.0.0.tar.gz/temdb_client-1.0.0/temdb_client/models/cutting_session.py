from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CuttingSessionBase(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    operator: Optional[str] = None
    sectioning_device: Optional[str] = None
    media_type: Optional[str] = None
    knife_id: Optional[str] = None
    block_id: Optional[str] = None
    specimen_id: Optional[str] = None

    class Config:
        extra = "allow"


class CuttingSessionCreate(CuttingSessionBase):
    cutting_session_id: str = Field(..., description="ID of cutting session")
    start_time: datetime = Field(..., description="Time when cutting session started")
    sectioning_device: str = Field(..., description="Device used for sectioning")
    media_type: str = Field(
        ..., description="Type of substrate the sections are placed upon"
    )
    block_id: str = Field(
        ..., description="ID of block cutting session is associated with"
    )


class CuttingSessionUpdate(CuttingSessionBase):
    pass


class CuttingSessionResponse(CuttingSessionBase):
    cutting_session_id: str = Field(..., description="Unique ID of cutting session")
    specimen_id: str = Field(..., description="Human-readable ID of specimen")
    block_id: str = Field(..., description="Human-readable ID of block")
    start_time: datetime
    sectioning_device: str
    media_type: str

    created_at: datetime
    updated_at: Optional[datetime] = None
