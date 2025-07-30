from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    """Type of resource in the registry."""

    MCP = "mcp"
    KNOWLEDGE_REPRESENTATION = "knowledge_representation"


class License(str, Enum):
    """License types for resources."""

    MIT = "MIT"
    APACHE2 = "Apache-2.0"
    GPL3 = "GPL-3.0"
    PROPRIETARY = "proprietary"


class MCPMetadata(BaseModel):
    """Metadata for MCP-compliant tools."""

    # Basic metadata
    identifier: Optional[str] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    version: str = Field(..., description="Tool version")

    # Tool metadata
    domain: str = Field(..., description="Domain of the tool (e.g., bioinformatics, cheminformatics)")
    data_types: list[str] = Field(..., description="Types of data the tool can process")
    format: str = Field(..., description="Implementation format (e.g., python, javascript)")
    size: int = Field(..., description="Size in bytes")
    license: License = Field(..., description="License type")

    # FAIR metadata
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    keywords: list[str] = Field(default_factory=list)
    authors: list[str] = Field(default_factory=list)

    # MCP-specific properties
    properties: dict[str, Any] = Field(
        default_factory=lambda: {
            "mcp_version": "1.0",
            "input_schema": "",
            "output_schema": "",
            "supported_models": [],
            "tool_capabilities": [],
        },
        description="MCP-specific properties",
    )


class KnowledgeRepresentationMetadata(BaseModel):
    """Metadata for knowledge representations."""

    # Basic metadata
    identifier: Optional[str] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Knowledge representation name")
    description: str = Field(..., description="Knowledge representation description")
    version: str = Field(..., description="Version")

    # Knowledge graph specific
    ontology_used: list[str] = Field(default_factory=list)
    node_types: list[str] = Field(default_factory=list)
    edge_types: list[str] = Field(default_factory=list)

    # Technical metadata
    format: str = Field(..., description="Storage format (e.g., neo4j, rdf)")
    size: int = Field(..., description="Size in bytes")
    license: License = Field(..., description="License type")

    # FAIR metadata
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    keywords: list[str] = Field(default_factory=list)
    authors: list[str] = Field(default_factory=list)

    # MCP integration properties
    properties: dict[str, Any] = Field(
        default_factory=lambda: {"mcp_compatible": False, "query_interface": "", "supported_tools": []},
        description="MCP integration properties",
    )
