"""
Example scripts demonstrating basic Neo4j operations.
"""

from typing import Dict, Any, List
from .database import Neo4jManager
from .config import Neo4jConfig


def create_sample_data() -> None:
    """Create sample data in the database."""
    manager = Neo4jManager()
    
    # Sample data creation queries
    queries = [
        # Create some people
        """
        CREATE (alice:Person {name: 'Alice', age: 30, city: 'New York'})
        CREATE (bob:Person {name: 'Bob', age: 25, city: 'San Francisco'})
        CREATE (charlie:Person {name: 'Charlie', age: 35, city: 'Chicago'})
        CREATE (diana:Person {name: 'Diana', age: 28, city: 'Boston'})
        """,
        
        # Create some companies
        """
        CREATE (techcorp:Company {name: 'TechCorp', industry: 'Technology'})
        CREATE (dataflow:Company {name: 'DataFlow', industry: 'Data Analytics'})
        CREATE (innovate:Company {name: 'Innovate Inc', industry: 'Consulting'})
        """,
        
        # Create relationships
        """
        MATCH (alice:Person {name: 'Alice'})
        MATCH (techcorp:Company {name: 'TechCorp'})
        CREATE (alice)-[:WORKS_FOR {since: 2020, position: 'Software Engineer'}]->(techcorp)
        """,
        
        """
        MATCH (bob:Person {name: 'Bob'})
        MATCH (dataflow:Company {name: 'DataFlow'})
        CREATE (bob)-[:WORKS_FOR {since: 2021, position: 'Data Scientist'}]->(dataflow)
        """,
        
        """
        MATCH (charlie:Person {name: 'Charlie'})
        MATCH (innovate:Company {name: 'Innovate Inc'})
        CREATE (charlie)-[:WORKS_FOR {since: 2019, position: 'Senior Consultant'}]->(innovate)
        """,
        
        # Create friendships
        """
        MATCH (alice:Person {name: 'Alice'})
        MATCH (bob:Person {name: 'Bob'})
        CREATE (alice)-[:FRIENDS_WITH {since: 2018}]->(bob)
        """,
        
        """
        MATCH (bob:Person {name: 'Bob'})
        MATCH (charlie:Person {name: 'Charlie'})
        CREATE (bob)-[:FRIENDS_WITH {since: 2020}]->(charlie)
        """,
        
        """
        MATCH (alice:Person {name: 'Alice'})
        MATCH (diana:Person {name: 'Diana'})
        CREATE (alice)-[:FRIENDS_WITH {since: 2019}]->(diana)
        """
    ]
    
    with manager.connection:
        for i, query in enumerate(queries, 1):
            print(f"Executing query {i}...")
            manager.connection.execute_write_query(query)
    
    print("Sample data created successfully!")


def query_examples() -> None:
    """Demonstrate various query examples."""
    manager = Neo4jManager()
    
    examples = [
        {
            "name": "Find all people",
            "query": "MATCH (p:Person) RETURN p.name, p.age, p.city ORDER BY p.name"
        },
        {
            "name": "Find all companies",
            "query": "MATCH (c:Company) RETURN c.name, c.industry ORDER BY c.name"
        },
        {
            "name": "Find people who work for companies",
            "query": """
            MATCH (p:Person)-[r:WORKS_FOR]->(c:Company)
            RETURN p.name, c.name, r.position, r.since
            ORDER BY p.name
            """
        },
        {
            "name": "Find friends of Alice",
            "query": """
            MATCH (alice:Person {name: 'Alice'})-[:FRIENDS_WITH]-(friend:Person)
            RETURN friend.name, friend.city
            ORDER BY friend.name
            """
        },
        {
            "name": "Count relationships by type",
            "query": """
            MATCH ()-[r]->()
            RETURN type(r) as relationship_type, count(r) as count
            ORDER BY count DESC
            """
        },
        {
            "name": "Find people in the same city",
            "query": """
            MATCH (p1:Person)-[:FRIENDS_WITH]-(p2:Person)
            WHERE p1.city = p2.city
            RETURN p1.name, p2.name, p1.city
            ORDER BY p1.city, p1.name
            """
        }
    ]
    
    with manager.connection:
        for example in examples:
            print(f"\n=== {example['name']} ===")
            try:
                results = manager.connection.execute_query(example['query'])
                for result in results:
                    print(result)
            except Exception as e:
                print(f"Error executing query: {e}")


def graph_analysis_examples() -> None:
    """Demonstrate graph analysis queries."""
    manager = Neo4jManager()
    
    analysis_queries = [
        {
            "name": "Degree centrality (number of connections)",
            "query": """
            MATCH (n:Person)
            OPTIONAL MATCH (n)-[r]-()
            RETURN n.name, count(r) as degree
            ORDER BY degree DESC
            """
        },
        {
            "name": "Find the most connected person",
            "query": """
            MATCH (n:Person)
            OPTIONAL MATCH (n)-[r]-()
            WITH n, count(r) as connections
            ORDER BY connections DESC
            LIMIT 1
            RETURN n.name, connections
            """
        },
        {
            "name": "Find people working in technology companies",
            "query": """
            MATCH (p:Person)-[:WORKS_FOR]->(c:Company)
            WHERE c.industry = 'Technology'
            RETURN p.name, c.name, c.industry
            ORDER BY p.name
            """
        },
        {
            "name": "Find mutual friends",
            "query": """
            MATCH (p1:Person)-[:FRIENDS_WITH]-(mutual:Person)-[:FRIENDS_WITH]-(p2:Person)
            WHERE p1 <> p2
            RETURN p1.name, p2.name, collect(mutual.name) as mutual_friends
            ORDER BY size(collect(mutual.name)) DESC
            """
        }
    ]
    
    with manager.connection:
        for analysis in analysis_queries:
            print(f"\n=== {analysis['name']} ===")
            try:
                results = manager.connection.execute_query(analysis['query'])
                for result in results:
                    print(result)
            except Exception as e:
                print(f"Error executing analysis: {e}")


def main() -> None:
    """Main function to run all examples."""
    print("=== Neo4j Learning Examples ===\n")
    
    # Test connection first
    manager = Neo4jManager()
    if not manager.test_connection():
        print("Failed to connect to Neo4j. Please ensure Neo4j is running.")
        return
    
    print("Connection successful!\n")
    
    # Create sample data
    print("Creating sample data...")
    create_sample_data()
    
    # Run query examples
    print("\nRunning query examples...")
    query_examples()
    
    # Run analysis examples
    print("\nRunning graph analysis examples...")
    graph_analysis_examples()
    
    print("\n=== Examples completed ===")


if __name__ == "__main__":
    main() 