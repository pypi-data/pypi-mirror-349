import asyncio
from typing import Any, List, Optional

from ...models.section import SectionResponse
from ...models.substrate import SubstrateCreate, SubstrateResponse, SubstrateUpdate
from ..substrate import SubstrateResource


class SyncSubstrateResourceWrapper:
    """
    Synchronous wrapper for the SubstrateResource.
    """

    def __init__(self, async_resource: SubstrateResource):
        self._async_resource = async_resource

    def list(
        self,
        media_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        **kwargs: Any
    ) -> List[SubstrateResponse]:
        """
        List substrates with optional filtering and pagination.
        """
        return asyncio.run(
            self._async_resource.list(
                media_type=media_type, status=status, skip=skip, limit=limit, **kwargs
            )
        )

    def create(self, substrate_data: SubstrateCreate) -> SubstrateResponse:
        """
        create a new substrate.
        """
        return asyncio.run(self._async_resource.create(substrate_data))

    def get(self, media_id: str) -> SubstrateResponse:
        """
        Get a specific substrate by ID.
        """
        return asyncio.run(self._async_resource.get(media_id))

    def update(
        self, media_id: str, substrate_data: SubstrateUpdate
    ) -> SubstrateResponse:
        """
        Update an existing substrate.
        """
        return asyncio.run(self._async_resource.update(media_id, substrate_data))

    def delete(self, media_id: str) -> None:
        """
        Delete a substrate.
        """
        return asyncio.run(self._async_resource.delete(media_id))

    def list_related_sections(
        self, media_id: str, skip: int = 0, limit: int = 100
    ) -> List[SectionResponse]:
        """
        List sections related to a specific substrate.
        """
        return asyncio.run(
            self._async_resource.list_related_sections(media_id, skip=skip, limit=limit)
        )
