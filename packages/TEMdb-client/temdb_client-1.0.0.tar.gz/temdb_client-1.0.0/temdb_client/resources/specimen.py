from typing import Any, List

from ..models.block import BlockResponse
from ..models.specimen import SpecimenCreate, SpecimenResponse, SpecimenUpdate
from .base import BaseResource


class SpecimenResource(BaseResource):
    """
    Resource class for interacting with Specimen endpoints.
    """

    async def list(
        self, skip: int = 0, limit: int = 100, **kwargs: Any
    ) -> List[SpecimenResponse]:
        """
        List specimens with optional pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            **kwargs: Additional parameters for the request.

        Returns:
            A list of SpecimenResponse objects.
        """
        params = {"skip": skip, "limit": limit}
        params.update(kwargs)
        response_data = await self._get("specimens", params=params)
        return (
            [SpecimenResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def create(self, specimen_data: SpecimenCreate) -> SpecimenResponse:
        """
        Create a new specimen.

        Args:
            specimen_data: A SpecimenCreate object containing the data for the new specimen.

        Returns:
            A SpecimenResponse object representing the created specimen.
        """
        response_data = await self._post(
            "specimens", data=specimen_data.model_dump(exclude_unset=True)
        )
        return SpecimenResponse.model_validate(response_data)

    async def get(self, specimen_id: str) -> SpecimenResponse:
        """
        Get a specific specimen by ID.

        Args:
            specimen_id: The human-readable ID of the specimen.

        Returns:
            A SpecimenResponse object representing the retrieved specimen.
        """
        response_data = await self._get(f"specimens/{specimen_id}")
        return SpecimenResponse.model_validate(response_data)

    async def update(
        self, specimen_id: str, specimen_data: SpecimenUpdate
    ) -> SpecimenResponse:
        """
        Update an existing specimen.

        Args:
            specimen_id: The human-readable ID of the specimen to update.
            specimen_data: A SpecimenUpdate object containing the fields to update.

        Returns:
            A SpecimenResponse object representing the updated specimen.
        """
        update_payload = specimen_data.model_dump(exclude_unset=True)
        response_data = await self._patch(
            f"specimens/{specimen_id}", data=update_payload
        )
        return SpecimenResponse.model_validate(response_data)

    async def delete(self, specimen_id: str) -> None:
        """
        Delete a specimen.

        Args:
            specimen_id: The human-readable ID of the specimen to delete.
        """
        await self._delete(f"specimens/{specimen_id}")

    async def add_image(self, specimen_id: str, image_url: str) -> SpecimenResponse:
        """
        Add an image URL to a specimen.

        Args:
            specimen_id: The human-readable ID of the specimen.
            image_url: The URL of the image to add.

        Returns:
            A SpecimenResponse object representing the updated specimen.
        """
        endpoint = f"specimens/{specimen_id}/images"
        payload = {"image_url": image_url}
        response_data = await self._post(endpoint, data=payload)
        return SpecimenResponse.model_validate(response_data)

    async def remove_image(self, specimen_id: str, image_url: str) -> SpecimenResponse:
        """
        Remove an image URL from a specimen.

        Args:
            specimen_id: The human-readable ID of the specimen.
            image_url: The URL of the image to remove.

        Returns:
            A SpecimenResponse object representing the updated specimen.
        """
        endpoint = f"specimens/{specimen_id}/images"
        params = {"image_url": image_url}
        response_data = await self._request("DELETE", endpoint, params=params)
        return SpecimenResponse.model_validate(response_data)

    async def list_blocks(
        self, specimen_id: str, skip: int = 0, limit: int = 100
    ) -> List[BlockResponse]:
        """
        List blocks associated with a specific specimen.

        Args:
            specimen_id: The human-readable ID of the specimen.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of BlockResponse objects.
        """
        endpoint = f"specimens/{specimen_id}/blocks"
        params = {"skip": skip, "limit": limit}
        response_data = await self._get(endpoint, params=params)
        return (
            [BlockResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )
