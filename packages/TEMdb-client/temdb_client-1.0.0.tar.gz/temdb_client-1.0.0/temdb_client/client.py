import httpx
import logging
import asyncio
from typing import Dict, Any, Optional, Union, List, cast

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from .resources.specimen import SpecimenResource
from .resources.block import BlockResource
from .resources.cutting_session import CuttingSessionResource
from .resources.substrate import SubstrateResource
from .resources.task import AcquisitionTaskResource
from .resources.roi import ROIResource
from .resources.acquisition import AcquisitionResource
from .resources.section import SectionResource

from .resources.sync_wrappers import (
    SyncAcquisitionResourceWrapper,
    SyncSpecimenResourceWrapper,
    SyncBlockResourceWrapper,
    SyncCuttingSessionResourceWrapper,
    SyncSubstrateResourceWrapper,
    SyncAcquisitionTaskResourceWrapper,
    SyncROIResourceWrapper,
    SyncSectionResourceWrapper,
)

from .exceptions import TEMdbClientError, NotFoundError


class AsyncTEMdbClient:
    """Asynchronous client for interacting with the TEMdb API."""

    def __init__(
        self,
        base_url: str,
        api_version: str = "v2",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        debug: bool = False,
    ):
        """Initialize the async client."""
        self.raw_base_url = base_url
        self.api_version = api_version
        self.api_url = f"{base_url}/api/{api_version}"
        self.api_key = api_key
        self.timeout = timeout

        self.logger = logging.getLogger("temdb_client.async")
        level = logging.DEBUG if debug else logging.INFO
        self.logger.setLevel(level)

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self._http_client = httpx.AsyncClient(
            base_url=self.api_url,
            headers=headers,
            timeout=timeout,
        )

        self.logger.info(
            f"Async TEMdb client initialized: {base_url} (API v{api_version})"
        )

        self._specimen = SpecimenResource(self._async_request, self.api_url)
        self._block = BlockResource(self._async_request, self.api_url)
        self._cutting_session = CuttingSessionResource(
            self._async_request, self.api_url
        )
        self._substrate = SubstrateResource(self._async_request, self.api_url)
        self._acquisition_task = AcquisitionTaskResource(
            self._async_request, self.api_url
        )
        self._roi = ROIResource(self._async_request, self.api_url)
        self._acquisition = AcquisitionResource(self._async_request, self.api_url)
        self._section = SectionResource(self._async_request, self.api_url)

    @property
    def specimen(self) -> SpecimenResource:
        """Access specimen-related async operations."""
        return self._specimen

    @property
    def block(self) -> BlockResource:
        """Access block-related async operations."""
        return self._block

    @property
    def cutting_session(self) -> CuttingSessionResource:
        """Access cutting session-related async operations."""
        return self._cutting_session

    @property
    def substrate(self) -> SubstrateResource:
        """Access substrate-related async operations."""
        return self._substrate

    @property
    def acquisition_task(self) -> AcquisitionTaskResource:  # Renamed property
        """Access acquisition task-related async operations."""
        return self._acquisition_task

    @property
    def roi(self) -> ROIResource:
        """Access ROI-related async operations."""
        return self._roi

    @property
    def acquisition(self) -> AcquisitionResource:
        """Access acquisition-related async operations."""
        return self._acquisition

    @property
    def section(self) -> SectionResource:
        """Access section-related async operations."""
        return self._section

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
    )
    async def _async_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Union[Dict[str, Any], List[Any]]:
        """Make an async HTTP request to the API."""
        self.logger.debug(f"Async Request: {method} {endpoint}")
        try:
            response = await self._http_client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()
        except httpx.HTTPStatusError as e:
            self.logger.error(
                f"HTTP error: {e.response.status_code} - {e.response.text}"
            )
            if e.response.status_code == 404:
                raise NotFoundError(f"Resource not found: {endpoint}") from e
            raise TEMdbClientError(
                f"HTTP {e.response.status_code}: {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise TEMdbClientError(f"Request failed: {str(e)}") from e
        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred during request to {endpoint}"
            )
            raise TEMdbClientError(f"Unexpected error: {str(e)}") from e

    async def health_check(self) -> Dict[str, Any]:
        """Check if the API is available."""
        try:
            result = await self._async_request("GET", "/health")
            self.logger.info(f"Async Health check: {result.get('status', 'unknown')}")
            return cast(Dict[str, Any], result)
        except Exception as e:
            self.logger.error(f"Async Health check failed: {str(e)}")
            raise

    async def get_api_info(self) -> Dict[str, Any]:
        """Get API information."""
        result = await self._async_request("GET", "/")
        return cast(Dict[str, Any], result)

    async def close(self) -> None:
        """Close the async client and release resources."""
        self.logger.info("Closing async TEMdb client")
        await self._http_client.aclose()

    async def __aenter__(self) -> "AsyncTEMdbClient":
        """Allow using client as async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close client when exiting async context manager."""
        await self.close()


class SyncTEMdbClient:
    """Synchronous client for interacting with the TEMdb API (wraps AsyncTEMdbClient)."""

    def __init__(
        self,
        base_url: str,
        api_version: str = "v2",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        debug: bool = False,
    ):
        """Initialize the sync client."""
        self._async_client = AsyncTEMdbClient(
            base_url, api_version, api_key, timeout, debug
        )
        self.logger = logging.getLogger("temdb_client.sync")
        level = logging.DEBUG if debug else logging.INFO
        self.logger.setLevel(level)
        self.logger.info(
            f"Sync TEMdb client initialized (wrapping async): {base_url} (API v{api_version})"
        )

        self._acquisition = SyncAcquisitionResourceWrapper(
            self._async_client.acquisition
        )
        self._specimen = SyncSpecimenResourceWrapper(self._async_client.specimen)
        self._block = SyncBlockResourceWrapper(self._async_client.block)
        self._cutting_session = SyncCuttingSessionResourceWrapper(
            self._async_client.cutting_session
        )
        self._substrate = SyncSubstrateResourceWrapper(self._async_client.substrate)
        self._acquisition_task = SyncAcquisitionTaskResourceWrapper(
            self._async_client.acquisition_task
        )
        self._roi = SyncROIResourceWrapper(self._async_client.roi)
        self._section = SyncSectionResourceWrapper(self._async_client.section)

    @property
    def acquisition(self) -> SyncAcquisitionResourceWrapper:
        """Access acquisition-related sync operations."""
        return self._acquisition

    @property
    def specimen(self) -> SyncSpecimenResourceWrapper:
        """Access specimen-related sync operations."""
        return self._specimen

    @property
    def block(self) -> SyncBlockResourceWrapper:
        """Access block-related sync operations."""
        return self._block

    @property
    def cutting_session(self) -> SyncCuttingSessionResourceWrapper:
        """Access cutting session-related sync operations."""
        return self._cutting_session

    @property
    def substrate(self) -> SyncSubstrateResourceWrapper:
        """Access substrate-related sync operations."""
        return self._substrate

    @property
    def acquisition_task(self) -> SyncAcquisitionTaskResourceWrapper:
        """Access acquisition task-related sync operations."""
        return self._acquisition_task

    @property
    def roi(self) -> SyncROIResourceWrapper:
        """Access ROI-related sync operations."""
        return self._roi

    @property
    def section(self) -> SyncSectionResourceWrapper:
        """Access section-related sync operations."""
        return self._section

    def health_check(self) -> Dict[str, Any]:
        """Check if the API is available."""
        self.logger.info("Running sync health check...")
        try:
            return asyncio.run(self._async_client.health_check())
        except Exception as e:
            self.logger.error(f"Sync Health check failed: {str(e)}")
            raise

    def get_api_info(self) -> Dict[str, Any]:
        """Get API information."""
        self.logger.info("Getting sync API info...")
        return asyncio.run(self._async_client.get_api_info())

    def close(self) -> None:
        """Close the client and release resources."""
        self.logger.info("Closing sync TEMdb client (and underlying async client)")
        asyncio.run(self._async_client.close())

    def __enter__(self) -> "SyncTEMdbClient":
        """Allow using client as sync context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close client when exiting sync context manager."""
        self.close()


def create_client(
    base_url: str,
    api_version: str = "v2",
    api_key: Optional[str] = None,
    timeout: float = 30.0,
    debug: bool = False,
    async_mode: bool = True,
) -> Union[AsyncTEMdbClient, SyncTEMdbClient]:
    """
    Factory function to create either an async or sync TEMdb client.

    Args:
        base_url: Base URL of the TEMdb API (e.g., "http://localhost:8000").
        api_version: API version string (default: "v2").
        api_key: Optional API key for authentication.
        timeout: Request timeout in seconds.
        debug: Enable debug logging for the client.
        async_mode: If True (default), returns AsyncTEMdbClient. If False, returns SyncTEMdbClient.

    Returns:
        An instance of AsyncTEMdbClient or SyncTEMdbClient.
    """
    if async_mode:
        return AsyncTEMdbClient(base_url, api_version, api_key, timeout, debug)
    else:
        return SyncTEMdbClient(base_url, api_version, api_key, timeout, debug)


if __name__ == "__main__":
    # Example usage
    client = create_client("http://localhost:8000", async_mode=False)
    try:
        info = client.get_api_info()
        print("API Info:", info)
    finally:
        client.close()

    # with context manager
    with create_client("http://localhost:8000", async_mode=False) as client:
        try:
            info = client.get_api_info()
            print("API Info:", info)
        except Exception as e:
            print(f"Error: {e}")

    # Example usage of async client
    async def main():
        async with create_client("http://localhost:8000", async_mode=True) as client:
            try:
                info = await client.get_api_info()
                print("API Info:", info)
            except Exception as e:
                print(f"Error: {e}")

    asyncio.run(main())
