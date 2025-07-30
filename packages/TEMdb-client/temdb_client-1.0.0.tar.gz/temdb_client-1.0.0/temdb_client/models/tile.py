from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Matcher(BaseModel):
    row: int
    col: int
    dX: float
    dY: float
    dXsd: float
    dYsd: float
    distance: float
    rotation: float
    match_quality: float
    position: int
    pX: List[float]
    pY: List[float]
    qX: List[float]
    qY: List[float]

    class Config:
        extra = "allow"


class TileBase(BaseModel):
    stage_position: Optional[Dict[str, float]] = None
    raster_position: Optional[Dict[str, int]] = None
    focus_score: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    mean_value: Optional[float] = None
    std_value: Optional[float] = None
    image_path: Optional[str] = None
    matcher: Optional[List[Matcher]] = None
    supertile_id: Optional[str] = None
    supertile_raster_position: Optional[Dict[str, int]] = None
    tile_id: Optional[str] = None
    raster_index: Optional[int] = None
    acquisition_id: Optional[str] = None

    class Config:
        extra = "allow"


class TileCreate(TileBase):
    tile_id: str = Field(...)
    raster_index: int = Field(...)
    stage_position: Dict[str, float] = Field(...)
    raster_position: Dict[str, int] = Field(...)
    focus_score: float = Field(...)
    min_value: float = Field(...)
    max_value: float = Field(...)
    mean_value: float = Field(...)
    std_value: float = Field(...)
    image_path: str = Field(...)


class TileUpdate(TileBase):
    pass


class TileResponse(TileBase):
    tile_id: str = Field(...)
    acquisition_id: str = Field(...)
    raster_index: int
    stage_position: Dict[str, float]
    raster_position: Dict[str, int]
    focus_score: float
    min_value: float
    max_value: float
    mean_value: float
    std_value: float
    image_path: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: Optional[int] = Field(
        None, description="Document version number"
    )
