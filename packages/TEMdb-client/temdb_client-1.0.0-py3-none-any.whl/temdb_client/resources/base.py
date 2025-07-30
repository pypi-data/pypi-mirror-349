import logging
from typing import Callable, Dict, Any


class BaseResource:
    def __init__(self, request_func: Callable, base_url: str):
        self._request = request_func
        self._base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)

    async def _get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return await self._request("GET", endpoint, **kwargs)

    async def _post(
        self, endpoint: str, data: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]:
        return await self._request("POST", endpoint, json=data, **kwargs)

    async def _patch(
        self, endpoint: str, data: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]:
        return await self._request("PATCH", endpoint, json=data, **kwargs)

    async def _delete(self, endpoint: str, **kwargs) -> None:
        await self._request("DELETE", endpoint, **kwargs)
