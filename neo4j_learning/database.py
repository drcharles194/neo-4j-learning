"""
Database connection module for Neo4j.
"""

from typing import Optional, Dict, Any, List
from neo4j import GraphDatabase, Driver, Session
from neo4j.exceptions import ServiceUnavailable, AuthError

from .config import Neo4jConfig


class Neo4jConnection:
    """Neo4j database connection manager."""
    
    def __init__(self, config: Optional[Neo4jConfig] = None):
        """
        Initialize Neo4j connection.
        
        Args:
            config: Neo4j configuration object
        """
        self.config = config or Neo4jConfig()
        self.driver: Optional[Driver] = None
    
    def connect(self) -> None:
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(
                self.config.uri,
                auth=(self.config.username, self.config.password)
            )
            # Verify connection
            self.driver.verify_connectivity()
            print(f"Successfully connected to Neo4j at {self.config.uri}")
        except ServiceUnavailable as e:
            print(f"Failed to connect to Neo4j: {e}")
            raise
        except AuthError as e:
            print(f"Authentication failed: {e}")
            raise
    
    def close(self) -> None:
        """Close the database connection."""
        if self.driver:
            self.driver.close()
            self.driver = None
            print("Neo4j connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def execute_query(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records
        """
        if not self.driver:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        with self.driver.session(database=self.config.database) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def execute_write_query(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a write Cypher query.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records
        """
        if not self.driver:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        with self.driver.session(database=self.config.database) as session:
            with session.begin_transaction() as tx:
                result = tx.run(query, parameters or {})
                records = [record.data() for record in result]
                tx.commit()
                return records


class Neo4jManager:
    """High-level Neo4j database manager."""
    
    def __init__(self, config: Optional[Neo4jConfig] = None):
        """
        Initialize Neo4j manager.
        
        Args:
            config: Neo4j configuration object
        """
        self.connection = Neo4jConnection(config)
    
    def test_connection(self) -> bool:
        """
        Test the database connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.connection:
                result = self.connection.execute_query("RETURN 1 as test")
                return len(result) > 0 and result[0]["test"] == 1
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get database information.
        
        Returns:
            Dictionary containing database information
        """
        with self.connection:
            result = self.connection.execute_query(
                "CALL dbms.components() YIELD name, versions, edition"
            )
            return result[0] if result else {}
    
    def clear_database(self) -> None:
        """Clear all data from the database."""
        with self.connection:
            self.connection.execute_write_query("MATCH (n) DETACH DELETE n")
            print("Database cleared") 