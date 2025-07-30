import asyncio
from typing import Any, List, Optional

from ...models.acquisition import AcquisitionResponse
from ...models.enum_schemas import AcquisitionTaskStatus
from ...models.task import (
    AcquisitionTaskCreate,
    AcquisitionTaskResponse,
    AcquisitionTaskUpdate,
)
from ..task import AcquisitionTaskResource


class SyncAcquisitionTaskResourceWrapper:
    """
    Synchronous wrapper for the AcquisitionTaskResource.
    """

    def __init__(self, async_resource: AcquisitionTaskResource):
        self._async_resource = async_resource

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[AcquisitionTaskStatus] = None,
        specimen_id: Optional[str] = None,
        block_id: Optional[str] = None,
        roi_id: Optional[int] = None,
        task_type: Optional[str] = None,
        **kwargs: Any
    ) -> List[AcquisitionTaskResponse]:
        """List acquisition tasks."""
        return asyncio.run(
            self._async_resource.list(
                skip=skip,
                limit=limit,
                status=status,
                specimen_id=specimen_id,
                block_id=block_id,
                roi_id=roi_id,
                task_type=task_type,
                **kwargs
            )
        )

    def create(self, task_data: AcquisitionTaskCreate) -> AcquisitionTaskResponse:
        """Create a new acquisition task."""
        return asyncio.run(self._async_resource.create(task_data))

    def get(
        self, task_id: str, version: Optional[int] = None
    ) -> AcquisitionTaskResponse:
        """Get a specific acquisition task by ID."""
        return asyncio.run(self._async_resource.get(task_id, version=version))

    def update(
        self, task_id: str, update_data: AcquisitionTaskUpdate
    ) -> AcquisitionTaskResponse:
        """Update an existing acquisition task."""
        return asyncio.run(self._async_resource.update(task_id, update_data))

    def delete(self, task_id: str) -> None:
        """Delete an acquisition task."""
        return asyncio.run(self._async_resource.delete(task_id))

    def list_related_acquisitions(
        self, task_id: str, skip: int = 0, limit: int = 100
    ) -> List[AcquisitionResponse]:
        """List acquisitions related to a specific task."""
        return asyncio.run(
            self._async_resource.list_related_acquisitions(
                task_id, skip=skip, limit=limit
            )
        )

    def update_status(
        self, task_id: str, status: AcquisitionTaskStatus
    ) -> AcquisitionTaskResponse:
        """Update the status of an acquisition task."""
        return asyncio.run(self._async_resource.update_status(task_id, status))

    def create_batch(
        self, tasks_data: List[AcquisitionTaskCreate]
    ) -> List[AcquisitionTaskResponse]:
        """Create a batch of acquisition tasks."""
        return asyncio.run(self._async_resource.create_batch(tasks_data))
