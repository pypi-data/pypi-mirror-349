from typing import Any, List, Optional

from ..models.enum_schemas import SectionQuality
from ..models.section import SectionCreate, SectionResponse, SectionUpdate
from .base import BaseResource


class SectionResource(BaseResource):
    """
    Resource class for interacting with Section endpoints.
    """

    async def list_by_session(
        self, cutting_session_id: str, skip: int = 0, limit: int = 100, **kwargs: Any
    ) -> List[SectionResponse]:
        """List sections associated with a specific cutting session."""
        endpoint = f"sections/sessions/{cutting_session_id}"
        params = {"skip": skip, "limit": limit}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def list_all(
        self,
        specimen_id: Optional[str] = None,
        block_id: Optional[str] = None,
        cutting_session_id: Optional[str] = None,
        media_id: Optional[str] = None,
        quality: Optional[SectionQuality] = None,
        skip: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> List[SectionResponse]:
        """List all sections, optionally filtering.

        Args:
            specimen_id (Optional[str]): The ID of the specimen to filter by.
            block_id (Optional[str]): The ID of the block to filter by.
            cutting_session_id (Optional[str]): The ID of the cutting session to filter by.
            media_id (Optional[str]): The ID of the media to filter by.
            quality (Optional[SectionQuality]): The quality of the section to filter by.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.
            **kwargs: Additional query parameters.

        Returns:
            List[SectionResponse]: A list of SectionResponse objects.

        """
        endpoint = "sections"
        params = {
            "specimen_id": specimen_id,
            "block_id": block_id,
            "cutting_session_id": cutting_session_id,
            "media_id": media_id,
            "quality": (quality.value if quality else None),
            "skip": skip,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def create(self, section_data: SectionCreate) -> SectionResponse:
        """Create a new section.

        Args:
            section_data (SectionCreate): A SectionCreate object containing the data for the new section.

        Returns:
            SectionResponse: A SectionResponse object representing the created section.

        """
        response_data = await self._post(
            "sections", data=section_data.model_dump(mode="json", exclude_unset=True)
        )
        return SectionResponse.model_validate(response_data)

    async def get(self, cutting_session_id: str, section_id: str) -> SectionResponse:
        """Get a specific section by session and section ID.

        Args:
            cutting_session_id (str): The ID of the cutting session.
            section_id (str): The ID of the section.

        Returns:
            SectionResponse: A SectionResponse object representing the retrieved section.

        """
        endpoint = f"sections/sessions/{cutting_session_id}/sections/{section_id}"
        response_data = await self._get(endpoint)
        return SectionResponse.model_validate(response_data)

    async def update(
        self, cutting_session_id: str, section_id: str, section_data: SectionUpdate
    ) -> SectionResponse:
        """Update an existing section.

        Args:
            cutting_session_id (str): The ID of the cutting session.
            section_id (str): The ID of the section to update.
            section_data (SectionUpdate): A SectionUpdate object containing the fields to update.

        Returns:
            SectionResponse: A SectionResponse object representing the updated section.

        """
        endpoint = f"sections/sessions/{cutting_session_id}/sections/{section_id}"
        update_payload = section_data.model_dump(exclude_unset=True)
        response_data = await self._patch(endpoint, data=update_payload)
        return SectionResponse.model_validate(response_data)

    async def delete(self, cutting_session_id: str, section_id: str) -> None:
        """Delete a section.

        Args:
            cutting_session_id (str): The ID of the cutting session.
            section_id (str): The ID of the section to delete.

        Returns:
            None: This method does not return anything.

        """
        endpoint = f"sections/sessions/{cutting_session_id}/sections/{section_id}"
        await self._delete(endpoint)

    async def list_by_block(
        self, block_id: str, skip: int = 0, limit: int = 100, **kwargs: Any
    ) -> List[SectionResponse]:
        """List sections associated with a specific block.

        Args:
            block_id (str): The ID of the block to filter by.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.
            **kwargs: Additional query parameters.

        Returns:
            List[SectionResponse]: A list of SectionResponse objects.

        """
        endpoint = f"sections/blocks/{block_id}"
        params = {"skip": skip, "limit": limit}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def list_by_specimen(
        self, specimen_id: str, skip: int = 0, limit: int = 100, **kwargs: Any
    ) -> List[SectionResponse]:
        """List sections associated with a specific specimen.

        Args:
            specimen_id (str): The ID of the specimen to filter by.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.
            **kwargs: Additional query parameters.

        Returns:
            List[SectionResponse]: A list of SectionResponse objects.

        """
        endpoint = f"sections/specimens/{specimen_id}"
        params = {"skip": skip, "limit": limit}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def list_by_media(
        self,
        media_id: str,
        skip: int = 0,
        limit: int = 100,
        relative_position: Optional[int] = None,
        **kwargs: Any,
    ) -> List[SectionResponse]:
        """List sections by media ID.

        Args:
            media_id (str): The ID of the media to filter by.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.
            relative_position (Optional[int]): Position relative to the media, if applicable.
            **kwargs: Additional query parameters.

        Returns:
            List[SectionResponse]: A list of SectionResponse objects.

        """
        endpoint = f"sections/media/{media_id}"
        params = {"skip": skip, "limit": limit, "relative_position": relative_position}
        params = {k: v for k, v in params.items() if v is not None}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def list_by_barcode(
        self, barcode: str, skip: int = 0, limit: int = 100, **kwargs: Any
    ) -> List[SectionResponse]:
        """List sections by barcode.

        Args:
            barcode (str): The barcode to filter sections by.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.
            **kwargs: Additional query parameters.

        Returns:
            List[SectionResponse]: A list of SectionResponse objects.

        """
        endpoint = f"sections/barcode/{barcode}"
        params = {"skip": skip, "limit": limit}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )
