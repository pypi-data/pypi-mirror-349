from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class BlockBase(BaseModel):
    microCT_info: Optional[Dict[str, Any]] = Field(
        None, description="MicroCT information of block"
    )

    class Config:
        extra = "allow"


class BlockCreate(BlockBase):
    block_id: str = Field(
        ..., description="Unique human-readable identifier for the block"
    )
    specimen_id: str = Field(
        ..., description="Human-readable identifier of the parent specimen"
    )
    microCT_info: Dict[str, Any] = Field(
        ..., description="MicroCT information of block"
    )


class BlockUpdate(BlockBase):
    pass


class BlockResponse(BlockBase):

    block_id: str = Field(
        ..., description="Unique human-readable identifier for the block"
    )
    specimen_id: str = Field(
        ..., description="Human-readable identifier of the parent specimen"
    )
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
