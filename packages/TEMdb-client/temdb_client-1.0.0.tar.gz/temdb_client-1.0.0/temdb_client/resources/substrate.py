from typing import List, Any, Optional
from .base import BaseResource

from ..models.substrate import SubstrateCreate, SubstrateUpdate, SubstrateResponse
from ..models.section import SectionResponse


class SubstrateResource(BaseResource):
    """
    Resource class for interacting with Substrate endpoints.
    """

    async def list(
        self,
        media_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> List[SubstrateResponse]:
        """
        List substrates with optional filtering and pagination.

        Args:
            media_type: Filter by substrate media type (e.g., 'wafer', 'tape').
            status: Filter by substrate status (e.g., 'new', 'used').
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            **kwargs: Additional parameters for the request.

        Returns:
            A list of SubstrateResponse objects.
        """
        params = {
            "media_type": media_type,
            "status": status,
            "skip": skip,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        params.update(kwargs)
        response_data = await self._get("substrates", params=params)
        return (
            [SubstrateResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def create(self, substrate_data: SubstrateCreate) -> SubstrateResponse:
        """
        Create a new substrate.

        Args:
            substrate_data: A SubstrateCreate object containing data for the new substrate.

        Returns:
            A SubstrateResponse object representing the created substrate.
        """
        response_data = await self._post(
            "substrates", data=substrate_data.model_dump(exclude_unset=True)
        )
        return SubstrateResponse.model_validate(response_data)

    async def get(self, media_id: str) -> SubstrateResponse:
        """
        Get a specific substrate by ID.

        Args:
            media_id: The human-readable ID of the substrate.

        Returns:
            A SubstrateResponse object representing the retrieved substrate.
        """
        response_data = await self._get(f"substrates/{media_id}")
        return SubstrateResponse.model_validate(response_data)

    async def update(
        self, media_id: str, substrate_data: SubstrateUpdate
    ) -> SubstrateResponse:
        """
        Update an existing substrate.

        Args:
            media_id: The human-readable ID of the substrate to update.
            substrate_data: A SubstrateUpdate object containing fields to update.

        Returns:
            A SubstrateResponse object representing the updated substrate.
        """
        update_payload = substrate_data.model_dump(exclude_unset=True)
        response_data = await self._patch(f"substrates/{media_id}", data=update_payload)
        return SubstrateResponse.model_validate(response_data)

    async def delete(self, media_id: str) -> None:
        """
        Delete a substrate.

        Args:
            media_id: The human-readable ID of the substrate to delete.
        """
        await self._delete(f"substrates/{media_id}")

    async def list_related_sections(
        self, media_id: str, skip: int = 0, limit: int = 100
    ) -> List[SectionResponse]:
        """
        List sections related to a specific substrate.

        Args:
            media_id: The human-readable ID of the substrate.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of SectionResponse objects.
        """
        endpoint = f"substrates/{media_id}/sections"
        params = {"skip": skip, "limit": limit}
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )
