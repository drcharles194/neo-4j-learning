"""
Tests for the configuration module.
"""

import os
import pytest
from unittest.mock import patch

from neo4j_learning.config import Neo4jConfig


class TestNeo4jConfig:
    """Test cases for Neo4jConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Neo4jConfig()
        
        assert config.uri == "bolt://localhost:7687"
        assert config.username == "neo4j"
        assert config.password == "password"
        assert config.database == "neo4j"
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = Neo4jConfig(
            uri="bolt://test:7687",
            username="testuser",
            password="testpass",
            database="testdb"
        )
        
        assert config.uri == "bolt://test:7687"
        assert config.username == "testuser"
        assert config.password == "testpass"
        assert config.database == "testdb"
    
    @patch.dict(os.environ, {
        'NEO4J_URI': 'bolt://env:7687',
        'NEO4J_USERNAME': 'envuser',
        'NEO4J_PASSWORD': 'envpass',
        'NEO4J_DATABASE': 'envdb'
    })
    def test_environment_variables(self):
        """Test configuration from environment variables."""
        config = Neo4jConfig()
        
        assert config.uri == "bolt://env:7687"
        assert config.username == "envuser"
        assert config.password == "envpass"
        assert config.database == "envdb"
    
    def test_repr(self):
        """Test string representation."""
        config = Neo4jConfig(
            uri="bolt://test:7687",
            username="testuser",
            database="testdb"
        )
        
        repr_str = repr(config)
        assert "Neo4jConfig" in repr_str
        assert "bolt://test:7687" in repr_str
        assert "testuser" in repr_str
        assert "testdb" in repr_str 