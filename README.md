# Neo4j Learning Repository

A comprehensive learning repository for Neo4j graph database development and Kubernetes integration. This project provides a structured environment for learning Neo4j with Python, including examples, utilities, and a command-line interface.

## Features

- 🚀 **Easy Setup**: Poetry-based dependency management with Neo4j driver
- 📚 **Learning Examples**: Comprehensive examples covering basic to advanced Neo4j operations
- 🔧 **CLI Tools**: Command-line interface for database operations
- 🧪 **Testing**: Unit tests and integration test examples
- 📖 **Documentation**: Well-documented code with type hints
- 🔒 **Configuration**: Environment-based configuration management

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- Neo4j Database (local or remote)

## Quick Start

### 1. Install Dependencies

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 2. Set Up Neo4j

#### Option A: Local Neo4j Installation

1. Download and install Neo4j Desktop or Neo4j Community Edition
2. Start Neo4j service
3. Set default password (usually 'password' for development)

#### Option B: Docker (Recommended for Development)

```bash
# Run Neo4j in Docker
docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/password \
    -e NEO4J_PLUGINS='["apoc"]' \
    neo4j:5.15.0

# Access Neo4j Browser at http://localhost:7474
```

### 3. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your Neo4j settings
# Default values work for local development
```

### 4. Test Connection

```bash
# Test database connection
poetry run python -m neo4j_learning.cli test
```

## Usage

### Command Line Interface

The project includes a comprehensive CLI for common operations:

```bash
# Test database connection
poetry run python -m neo4j_learning.cli test

# Run learning examples
poetry run python -m neo4j_learning.cli examples

# Start interactive mode for Cypher queries
poetry run python -m neo4j_learning.cli interactive

# Clear all data from database
poetry run python -m neo4j_learning.cli clear
```

### Interactive Mode

Start an interactive session to run Cypher queries:

```bash
poetry run python -m neo4j_learning.cli interactive
```

Example queries in interactive mode:
```cypher
MATCH (n) RETURN n LIMIT 5
MATCH (p:Person) RETURN p.name, p.age
MATCH ()-[r]->() RETURN type(r), count(r)
```

### Python API

Use the Python API in your own scripts:

```python
from neo4j_learning.database import Neo4jManager
from neo4j_learning.config import Neo4jConfig

# Create custom configuration
config = Neo4jConfig(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="your_password"
)

# Initialize manager
manager = Neo4jManager(config)

# Test connection
if manager.test_connection():
    print("Connected successfully!")
    
    # Execute queries
    results = manager.connection.execute_query(
        "MATCH (n:Person) RETURN n.name LIMIT 5"
    )
    print(results)
```

## Project Structure

```
neo-4j-learning/
├── neo4j_learning/          # Main package
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Configuration management
│   ├── database.py         # Database connection and operations
│   ├── examples.py         # Learning examples
│   └── cli.py             # Command-line interface
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_config.py     # Configuration tests
├── pyproject.toml         # Poetry configuration
├── .gitignore            # Git ignore rules
├── env.example           # Environment template
└── README.md            # This file
```

## Learning Examples

The project includes comprehensive examples covering:

- **Basic Operations**: Creating nodes, relationships, and properties
- **Querying**: MATCH, WHERE, RETURN, ORDER BY, LIMIT
- **Graph Analysis**: Degree centrality, path finding, community detection
- **Data Import**: Loading data from various sources
- **Performance**: Indexing, query optimization

Run examples:
```bash
poetry run python -m neo4j_learning.examples
```

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=neo4j_learning

# Run specific test file
poetry run pytest tests/test_config.py
```

### Code Quality

```bash
# Format code
poetry run black neo4j_learning/ tests/

# Lint code
poetry run flake8 neo4j_learning/ tests/

# Type checking
poetry run mypy neo4j_learning/
```

### Adding New Features

1. Create feature branch
2. Add tests for new functionality
3. Implement feature with proper documentation
4. Run tests and quality checks
5. Submit pull request

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j connection URI |
| `NEO4J_USERNAME` | `neo4j` | Database username |
| `NEO4J_PASSWORD` | `password` | Database password |
| `NEO4J_DATABASE` | `neo4j` | Database name |

### Custom Configuration

```python
from neo4j_learning.config import Neo4jConfig

# Create custom configuration
config = Neo4jConfig(
    uri="bolt://your-neo4j:7687",
    username="your_username",
    password="your_password",
    database="your_database"
)
```

## Troubleshooting

### Connection Issues

1. **Service Unavailable**: Ensure Neo4j is running
2. **Authentication Failed**: Check username/password
3. **Port Issues**: Verify Neo4j is listening on correct port (7687)

### Common Commands

```bash
# Check Neo4j status (Docker)
docker ps | grep neo4j

# View Neo4j logs (Docker)
docker logs neo4j

# Reset Neo4j password
docker exec -it neo4j neo4j-admin set-initial-password newpassword
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [Neo4j Python Driver Documentation](https://neo4j.com/docs/python-manual/current/)
- [Cypher Query Language](https://neo4j.com/docs/cypher-manual/current/)
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/)
- [Neo4j Kubernetes](https://neo4j.com/docs/operations-manual/current/kubernetes/)
