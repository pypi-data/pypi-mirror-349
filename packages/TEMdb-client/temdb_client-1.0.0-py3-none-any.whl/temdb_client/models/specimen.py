from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SpecimenBase(BaseModel):

    description: Optional[str] = Field(
        None, description="Description of specimen, used for additional notes."
    )
    specimen_images: Optional[List[str]] = Field(
        None, description="List of image URLs associated with the specimen"
    )
    functional_imaging_metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Functional imaging metadata of specimen, optional links to other datasets",
    )

    class Config:
        extra = "allow"


class SpecimenCreate(SpecimenBase):
    specimen_id: str = Field(
        ..., description="Unique human-readable identifier for the specimen"
    )


class SpecimenUpdate(SpecimenBase):
    pass


class SpecimenResponse(SpecimenBase):
    """
    Model representing a Specimen object as returned by the API (GET requests).
    Based on the server's Specimen Document model.
    """

    specimen_id: str = Field(
        ..., description="Unique human-readable identifier for the specimen"
    )
    specimen_images: List[str] = Field(
        default_factory=list,
        description="List of image URLs associated with the specimen",
    )
    created_at: datetime
    updated_at: Optional[datetime] = None
