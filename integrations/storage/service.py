"""Storage service factory and manager."""

import os
from typing import Optional

from integrations.storage.base import BaseStorageProvider
from integrations.storage.models import StorageProviderType
from integrations.storage.providers.local import LocalFileStorageProvider
from integrations.storage.providers.mock import MockStorageProvider


class StorageService:
    """Unified storage service coordinating providers."""

    _instance: Optional["StorageService"] = None

    def __init__(self, provider: Optional[BaseStorageProvider] = None) -> None:
        if provider is not None:
            self._provider = provider
        else:
            provider_type = os.getenv("STORAGE_PROVIDER", "local").lower()
            if provider_type == "mock":
                self._provider = MockStorageProvider()
            else:
                base_path = os.getenv("STORAGE_LOCAL_PATH", "./storage")
                self._provider = LocalFileStorageProvider(base_path=base_path)

    @property
    def provider(self) -> BaseStorageProvider:
        return self._provider

    @classmethod
    def get_instance(cls) -> "StorageService":
        if cls._instance is None:
            cls._instance = StorageService()
        return cls._instance

    @classmethod
    def set_instance(cls, instance: "StorageService") -> None:
        cls._instance = instance
