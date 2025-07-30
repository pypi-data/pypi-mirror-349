import uuid
from typing import Any, Optional, Union

from .schema import KnowledgeRepresentationMetadata, MCPMetadata, ResourceType


class RegistryError(Exception):
    """Custom exception for registry-related errors."""

    MCP_NOT_FOUND = "MCP tool not found: {}"
    KR_NOT_FOUND = "Knowledge representation not found: {}"

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message.format(*args) if args else message)


class RegistryClient:
    """Client for interacting with the BioContext registry."""

    def __init__(self, base_url: str) -> None:
        """Initialize the registry client.

        Args:
            base_url: Base URL of the registry API
        """
        self.base_url = base_url.rstrip("/")
        # For testing purposes, we'll store metadata in memory
        self._mcp_store: dict[str, MCPMetadata] = {}
        self._kr_store: dict[str, KnowledgeRepresentationMetadata] = {}

    async def register_mcp(self, metadata: MCPMetadata) -> str:
        """Register a new MCP tool.

        Args:
            metadata: MCP tool metadata

        Returns:
            str: Tool identifier
        """
        identifier = metadata.identifier or str(uuid.uuid4())
        self._mcp_store[identifier] = metadata
        return identifier

    async def register_knowledge_representation(self, metadata: KnowledgeRepresentationMetadata) -> str:
        """Register a new knowledge representation.

        Args:
            metadata: Knowledge representation metadata

        Returns:
            str: Knowledge representation identifier
        """
        identifier = metadata.identifier or str(uuid.uuid4())
        self._kr_store[identifier] = metadata
        return identifier

    async def search(
        self,
        query: str,
        resource_type: Optional[ResourceType] = None,
        filters: Optional[dict[str, Any]] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Union[MCPMetadata, KnowledgeRepresentationMetadata]]:
        """Search for resources in the registry.

        Args:
            query: Search query string
            resource_type: Type of resource to search for
            filters: Additional filters to apply
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            List of matching resources
        """
        results: list[Union[MCPMetadata, KnowledgeRepresentationMetadata]] = []

        # Search MCP tools
        if resource_type in [None, ResourceType.MCP]:
            for metadata in self._mcp_store.values():
                if self._matches_filters(metadata, query, filters):
                    results.append(metadata)

        # Search knowledge representations
        if resource_type in [None, ResourceType.KNOWLEDGE_REPRESENTATION]:
            for kr_metadata in self._kr_store.values():
                if self._matches_filters(kr_metadata, query, filters):
                    results.append(kr_metadata)

        # Apply pagination
        return results[offset : offset + limit]

    async def get_mcp(self, identifier: str) -> MCPMetadata:
        """Get MCP tool metadata by identifier.

        Args:
            identifier: Tool identifier

        Returns:
            MCP tool metadata

        Raises:
            RegistryError: If tool is not found
        """
        if identifier not in self._mcp_store:
            raise RegistryError(RegistryError.MCP_NOT_FOUND, identifier)
        return self._mcp_store[identifier]

    async def get_knowledge_representation(self, identifier: str) -> KnowledgeRepresentationMetadata:
        """Get knowledge representation metadata by identifier.

        Args:
            identifier: Knowledge representation identifier

        Returns:
            Knowledge representation metadata

        Raises:
            RegistryError: If knowledge representation is not found
        """
        if identifier not in self._kr_store:
            raise RegistryError(RegistryError.KR_NOT_FOUND, identifier)
        return self._kr_store[identifier]

    async def update_metadata(
        self,
        identifier: str,
        metadata: Union[MCPMetadata, KnowledgeRepresentationMetadata],
    ) -> bool:
        """Update resource metadata.

        Args:
            identifier: Resource identifier
            metadata: Updated metadata

        Returns:
            bool: True if update was successful

        Raises:
            RegistryError: If resource is not found
        """
        if isinstance(metadata, MCPMetadata):
            if identifier not in self._mcp_store:
                raise RegistryError(RegistryError.MCP_NOT_FOUND, identifier)
            self._mcp_store[identifier] = metadata
        else:
            if identifier not in self._kr_store:
                raise RegistryError(RegistryError.KR_NOT_FOUND, identifier)
            self._kr_store[identifier] = metadata
        return True

    def _matches_filters(
        self,
        metadata: Union[MCPMetadata, KnowledgeRepresentationMetadata],
        query: str,
        filters: Optional[dict[str, Any]] = None,
    ) -> bool:
        """Check if metadata matches the search query and filters.

        Args:
            metadata: Resource metadata
            query: Search query string
            filters: Additional filters to apply

        Returns:
            bool: True if metadata matches
        """
        # Basic text search
        searchable_fields = [
            metadata.name,
            metadata.description,
            *metadata.keywords,
        ]
        if not any(query.lower() in field.lower() for field in searchable_fields):
            return False

        # Apply filters
        if filters:
            for key, value in filters.items():
                if key.startswith("properties."):
                    prop_key = key.split(".", 1)[1]
                    if prop_key not in metadata.properties:
                        return False
                    if metadata.properties[prop_key] != value:
                        return False
                else:
                    if not hasattr(metadata, key):
                        return False
                    if getattr(metadata, key) != value:
                        return False

        return True
