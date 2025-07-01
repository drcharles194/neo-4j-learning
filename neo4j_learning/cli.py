"""
Command-line interface for Neo4j operations.
"""

import argparse
import sys, readline
from typing import Optional

from .database import Neo4jManager
from .config import Neo4jConfig
from .examples import create_sample_data, query_examples, graph_analysis_examples


def test_connection() -> None:
    """Test the Neo4j connection."""
    manager = Neo4jManager()
    if manager.test_connection():
        print("✅ Connection successful!")
        
        # Get database info
        info = manager.get_database_info()
        if info:
            print(f"Database: {info.get('name', 'Unknown')}")
            print(f"Version: {info.get('versions', ['Unknown'])[0]}")
            print(f"Edition: {info.get('edition', 'Unknown')}")
    else:
        print("❌ Connection failed!")
        sys.exit(1)


def clear_database() -> None:
    """Clear all data from the database."""
    manager = Neo4jManager()
    if manager.test_connection():
        confirm = input("Are you sure you want to clear all data? (yes/no): ")
        if confirm.lower() == 'yes':
            manager.clear_database()
            print("✅ Database cleared!")
        else:
            print("Operation cancelled.")
    else:
        print("❌ Cannot connect to database!")
        sys.exit(1)


def run_examples() -> None:
    """Run the example scripts."""
    from .examples import main
    main()


def interactive_mode() -> None:
    """Start interactive mode for running Cypher queries."""
    manager = Neo4jManager()
    
    if not manager.test_connection():
        print("❌ Cannot connect to database!")
        sys.exit(1)
    
    print("=== Neo4j Interactive Mode ===")
    print("Enter Cypher queries (type 'quit' to exit)")
    print("Type 'help' for some example queries\n")
    
    with manager.connection:
        while True:
            try:
                query = input("neo4j> ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if query.lower() == 'help':
                    print_help()
                    continue
                
                if not query:
                    continue
                
                # Execute query
                results = manager.connection.execute_query(query)
                
                if results:
                    print(f"\nResults ({len(results)} records):")
                    for i, result in enumerate(results, 1):
                        print(f"  {i}. {result}")
                else:
                    print("No results returned.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def print_help() -> None:
    """Print help information for interactive mode."""
    help_text = """
Available commands:
  quit, exit, q  - Exit interactive mode
  help          - Show this help message

Example queries:
  MATCH (n) RETURN n LIMIT 5
  MATCH (p:Person) RETURN p.name, p.age
  MATCH ()-[r]->() RETURN type(r), count(r)
  MATCH (n) RETURN labels(n), count(n)
    """
    print(help_text)


def main() -> None:
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Neo4j Learning CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m neo4j_learning.cli test          # Test connection
  python -m neo4j_learning.cli examples      # Run examples
  python -m neo4j_learning.cli interactive   # Start interactive mode
  python -m neo4j_learning.cli clear         # Clear database
        """
    )
    
    parser.add_argument(
        'command',
        choices=['test', 'examples', 'interactive', 'clear'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--uri',
        help='Neo4j URI (default: bolt://localhost:7687)'
    )
    
    parser.add_argument(
        '--username',
        help='Neo4j username (default: neo4j)'
    )
    
    parser.add_argument(
        '--password',
        help='Neo4j password (default: password)'
    )
    
    parser.add_argument(
        '--database',
        help='Neo4j database name (default: neo4j)'
    )
    
    args = parser.parse_args()
    
    # Create custom config if arguments provided
    config = None
    if any([args.uri, args.username, args.password, args.database]):
        config = Neo4jConfig(
            uri=args.uri,
            username=args.username,
            password=args.password,
            database=args.database
        )
    
    # Execute command
    if args.command == 'test':
        test_connection()
    elif args.command == 'examples':
        run_examples()
    elif args.command == 'interactive':
        interactive_mode()
    elif args.command == 'clear':
        clear_database()


if __name__ == "__main__":
    main() 