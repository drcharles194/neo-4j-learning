"""
Configuration module for Neo4j connection settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Neo4jConfig:
    """Configuration class for Neo4j connection settings."""
    
    def __init__(
        self,
        uri: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ):
        """
        Initialize Neo4j configuration.
        
        Args:
            uri: Neo4j connection URI
            username: Neo4j username
            password: Neo4j password
            database: Neo4j database name
        """
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = username or os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.database = database or os.getenv("NEO4J_DATABASE", "neo4j")
    
    def __repr__(self) -> str:
        """String representation of the configuration."""
        return (
            f"Neo4jConfig(uri='{self.uri}', "
            f"username='{self.username}', "
            f"database='{self.database}')"
        )


# Default configuration instance
default_config = Neo4jConfig() 