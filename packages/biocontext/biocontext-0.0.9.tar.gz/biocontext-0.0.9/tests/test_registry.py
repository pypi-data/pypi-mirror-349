import pytest

from biocontext.registry.client import RegistryClient, RegistryError
from biocontext.registry.schema import (
    KnowledgeRepresentationMetadata,
    License,
    MCPMetadata,
    ResourceType,
)


@pytest.fixture
def sample_mcp_metadata():
    return MCPMetadata(
        identifier="test-tool-001",
        name="Test MCP Tool",
        description="A test MCP-compliant tool for unit testing",
        version="1.0.0",
        domain="bioinformatics",
        data_types=["sequence", "structure"],
        format="python",
        size=1024,
        license=License.MIT,
        doi="10.1234/test.001",
        keywords=["test", "sequence analysis", "structure prediction"],
        authors=["Test Author"],
        properties={
            "mcp_version": "1.0",
            "input_schema": "protein_sequence",
            "output_schema": "protein_structure",
            "supported_models": ["gpt-4", "claude-3"],
            "tool_capabilities": ["sequence_analysis", "structure_prediction"],
        },
    )


@pytest.fixture
def sample_kr_metadata():
    return KnowledgeRepresentationMetadata(
        identifier="test-kr-001",
        name="Test Knowledge Graph",
        description="A test knowledge graph for use with MCP tools",
        version="1.0.0",
        ontology_used=["GO", "HPO"],
        node_types=["Gene", "Disease", "Phenotype"],
        edge_types=["ASSOCIATED_WITH", "ENCODES"],
        format="neo4j",
        size=2048,
        license=License.APACHE2,
        doi="10.1234/test.002",
        keywords=["test", "knowledge graph", "disease"],
        authors=["Test Author"],
        properties={"mcp_compatible": True, "query_interface": "cypher", "supported_tools": ["test-tool-001"]},
    )


@pytest.fixture
def registry_client():
    return RegistryClient("http://localhost:8000")


class TestMCPMetadata:
    def test_mcp_metadata_creation(self, sample_mcp_metadata):
        assert sample_mcp_metadata.identifier == "test-tool-001"
        assert sample_mcp_metadata.name == "Test MCP Tool"
        assert sample_mcp_metadata.domain == "bioinformatics"
        assert sample_mcp_metadata.license == License.MIT
        assert sample_mcp_metadata.properties["mcp_version"] == "1.0"
        assert "sequence_analysis" in sample_mcp_metadata.properties["tool_capabilities"]

    def test_mcp_metadata_optional_fields(self):
        metadata = MCPMetadata(
            identifier="minimal-tool",
            name="Minimal MCP Tool",
            description="Minimal test case",
            version="1.0.0",
            domain="bioinformatics",
            data_types=["sequence"],
            format="python",
            size=1024,
            license=License.MIT,
            properties={
                "mcp_version": "1.0",
                "input_schema": "sequence",
                "output_schema": "analysis",
                "supported_models": ["gpt-4"],
                "tool_capabilities": ["basic_analysis"],
            },
        )
        assert metadata.doi is None
        assert metadata.keywords == []
        assert metadata.authors == []


class TestKnowledgeRepresentationMetadata:
    def test_kr_metadata_creation(self, sample_kr_metadata):
        assert sample_kr_metadata.identifier == "test-kr-001"
        assert sample_kr_metadata.name == "Test Knowledge Graph"
        assert "GO" in sample_kr_metadata.ontology_used
        assert "Gene" in sample_kr_metadata.node_types
        assert sample_kr_metadata.license == License.APACHE2
        assert sample_kr_metadata.properties["mcp_compatible"] is True
        assert "test-tool-001" in sample_kr_metadata.properties["supported_tools"]

    def test_kr_metadata_optional_fields(self):
        metadata = KnowledgeRepresentationMetadata(
            identifier="minimal-kr",
            name="Minimal KR",
            description="Minimal test case",
            version="1.0.0",
            format="neo4j",
            size=2048,
            license=License.MIT,
            properties={"mcp_compatible": True, "query_interface": "cypher"},
        )
        assert metadata.ontology_used == []
        assert metadata.node_types == []
        assert metadata.edge_types == []
        assert metadata.doi is None


class TestRegistryClient:
    @pytest.mark.asyncio
    async def test_register_mcp(self, registry_client, sample_mcp_metadata):
        # This is a mock test - actual implementation will depend on backend
        identifier = await registry_client.register_mcp(sample_mcp_metadata)
        assert isinstance(identifier, str)
        assert len(identifier) > 0

    @pytest.mark.asyncio
    async def test_register_kr(self, registry_client, sample_kr_metadata):
        # This is a mock test - actual implementation will depend on backend
        identifier = await registry_client.register_knowledge_representation(sample_kr_metadata)
        assert isinstance(identifier, str)
        assert len(identifier) > 0

    @pytest.mark.asyncio
    async def test_search(self, registry_client, sample_mcp_metadata):
        # Register a tool first
        await registry_client.register_mcp(sample_mcp_metadata)

        # Search for the tool
        results = await registry_client.search(
            query="sequence analysis",
            resource_type=ResourceType.MCP,
            filters={"domain": "bioinformatics", "properties.mcp_version": "1.0"},
            limit=5,
            offset=0,
        )
        assert isinstance(results, list)
        assert len(results) > 0
        assert results[0].identifier == sample_mcp_metadata.identifier

    @pytest.mark.asyncio
    async def test_get_mcp(self, registry_client, sample_mcp_metadata):
        # Register the MCP tool first
        await registry_client.register_mcp(sample_mcp_metadata)

        # Now try to get it
        metadata = await registry_client.get_mcp("test-tool-001")
        assert isinstance(metadata, MCPMetadata)
        assert metadata.identifier == sample_mcp_metadata.identifier
        assert metadata.name == sample_mcp_metadata.name
        assert metadata.domain == sample_mcp_metadata.domain

    @pytest.mark.asyncio
    async def test_get_nonexistent_mcp(self, registry_client):
        # Test getting a non-existent MCP tool
        with pytest.raises(RegistryError) as exc_info:
            await registry_client.get_mcp("nonexistent-tool")
        assert "MCP tool not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_kr(self, registry_client, sample_kr_metadata):
        # Register the knowledge representation first
        await registry_client.register_knowledge_representation(sample_kr_metadata)

        # Now try to get it
        metadata = await registry_client.get_knowledge_representation("test-kr-001")
        assert isinstance(metadata, KnowledgeRepresentationMetadata)
        assert metadata.identifier == sample_kr_metadata.identifier
        assert metadata.name == sample_kr_metadata.name
        assert metadata.properties["mcp_compatible"] == sample_kr_metadata.properties["mcp_compatible"]

    @pytest.mark.asyncio
    async def test_get_nonexistent_kr(self, registry_client):
        # Test getting a non-existent knowledge representation
        with pytest.raises(RegistryError) as exc_info:
            await registry_client.get_knowledge_representation("nonexistent-kr")
        assert "Knowledge representation not found" in str(exc_info.value)
