from typing import List, Optional, Any
from .base import BaseResource

from ..models.cutting_session import (
    CuttingSessionCreate,
    CuttingSessionUpdate,
    CuttingSessionResponse,
)
from ..models.section import SectionResponse


class CuttingSessionResource(BaseResource):
    """
    Resource class for interacting with Cutting Session endpoints.
    """

    async def list_by_block(
        self,
        specimen_id: str,
        block_id: str,
        skip: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> List[CuttingSessionResponse]:
        """List cutting sessions associated with a specific block.

        Args:
            specimen_id (str): The ID of the specimen.
            block_id (str): The ID of the block.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.
            **kwargs: Additional query parameters.

        Returns:
            List[CuttingSessionResponse]: A list of CuttingSessionResponse objects.

        """
        endpoint = (
            f"cutting-sessions/specimens/{specimen_id}/blocks/{block_id}/sessions"
        )
        params = {"skip": skip, "limit": limit}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [CuttingSessionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def list_all(
        self,
        specimen_id: Optional[str] = None,
        block_id: Optional[str] = None,
        operator: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> List[CuttingSessionResponse]:
        """List all cutting sessions, optionally filtering.

        Args:
            specimen_id (Optional[str]): The ID of the specimen to filter by.
            block_id (Optional[str]): The ID of the block to filter by.
            operator (Optional[str]): The operator associated with the sessions.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.
            **kwargs: Additional query parameters.

        Returns:
            List[CuttingSessionResponse]: A list of CuttingSessionResponse objects.

        Example:
            Example 1 without additional parameters:
            await cutting_session_resource.list_all(specimen_id="specimen123", block_id="block456", operator="operator789")

            Example 2 using the `kwargs` parameter:
            await cutting_session_resource.list_all(specimen_id="specimen123", block_id="block456", operator="operator789", custom_param="value")


        """
        endpoint = "cutting-sessions"
        params = {
            "skip": skip,
            "limit": limit,
            "specimen_id": specimen_id,
            "block_id": block_id,
            "operator": operator,
        }
        params = {k: v for k, v in params.items() if v is not None}
        params.update(kwargs)
        response_data = await self._get(endpoint, params=params)
        return (
            [CuttingSessionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )

    async def create(
        self, session_data: CuttingSessionCreate
    ) -> CuttingSessionResponse:
        """Create a new cutting session.

        Args:
            session_data (CuttingSessionCreate): A CuttingSessionCreate object containing the data for the new session.

        Returns:
            CuttingSessionResponse: A CuttingSessionResponse object representing the created session.

        """
        response_data = await self._post(
            "cutting-sessions",
            data=session_data.model_dump(mode="json", exclude_unset=True),
        )
        return CuttingSessionResponse.model_validate(response_data)

    async def get(
        self, specimen_id: str, block_id: str, cutting_session_id: str
    ) -> CuttingSessionResponse:
        """Get a specific cutting session by specimen, block, and session ID.

        Args:
            specimen_id (str): The ID of the specimen.
            block_id (str): The ID of the block.
            cutting_session_id (str): The ID of the cutting session.

        Returns:
            CuttingSessionResponse: A CuttingSessionResponse object representing the retrieved session.

        """
        endpoint = f"cutting-sessions/specimens/{specimen_id}/blocks/{block_id}/sessions/{cutting_session_id}"
        response_data = await self._get(endpoint)
        return CuttingSessionResponse.model_validate(response_data)

    async def update(
        self, cutting_session_id: str, session_data: CuttingSessionUpdate
    ) -> CuttingSessionResponse:
        """Update an existing cutting session.

        Args:
            cutting_session_id (str): The ID of the cutting session to update.
            session_data (CuttingSessionUpdate): A CuttingSessionUpdate object containing the fields to update.

        Returns:
            CuttingSessionResponse: A CuttingSessionResponse object representing the updated session.

        """
        endpoint = f"cutting-sessions/{cutting_session_id}"
        update_payload = session_data.model_dump(exclude_unset=True)
        response_data = await self._patch(endpoint, data=update_payload)
        return CuttingSessionResponse.model_validate(response_data)

    async def delete(self, cutting_session_id: str) -> None:
        """Delete a cutting session.

        Args:
            cutting_session_id (str): The ID of the cutting session to delete.

        Returns:
            None: This method does not return anything.

        """
        endpoint = f"cutting-sessions/{cutting_session_id}"
        await self._delete(endpoint)

    async def list_sections(
        self,
        specimen_id: str,
        block_id: str,
        cutting_session_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[SectionResponse]:
        """List sections associated with a specific cutting session.

        Args:
            specimen_id (str): The ID of the specimen.
            block_id (str): The ID of the block.
            cutting_session_id (str): The ID of the cutting session.
            skip (int): Number of items to skip for pagination.
            limit (int): Maximum number of items to return.

        Returns:
            List[SectionResponse]: A list of SectionResponse objects representing the sections.


        """
        endpoint = f"cutting-sessions/specimens/{specimen_id}/blocks/{block_id}/sessions/{cutting_session_id}/sections"
        params = {"skip": skip, "limit": limit}
        response_data = await self._get(endpoint, params=params)
        return (
            [SectionResponse.model_validate(item) for item in response_data]
            if isinstance(response_data, list)
            else []
        )
