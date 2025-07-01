#!/usr/bin/env python3
"""
Setup script for Neo4j Learning Repository.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a shell command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def check_poetry() -> bool:
    """Check if Poetry is installed."""
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_poetry() -> bool:
    """Install Poetry if not already installed."""
    if check_poetry():
        print("✅ Poetry is already installed")
        return True
    
    print("📦 Installing Poetry...")
    install_command = "curl -sSL https://install.python-poetry.org | python3 -"
    return run_command(install_command, "Installing Poetry")


def setup_environment() -> bool:
    """Set up environment file."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    try:
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your Neo4j settings")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def install_dependencies() -> bool:
    """Install project dependencies using Poetry."""
    return run_command("poetry install", "Installing dependencies")


def run_tests() -> bool:
    """Run the test suite."""
    return run_command("poetry run pytest tests/ -v", "Running tests")


def main():
    """Main setup function."""
    print("🚀 Setting up Neo4j Learning Repository")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install Poetry
    if not install_poetry():
        print("❌ Failed to install Poetry")
        sys.exit(1)
    
    # Set up environment
    if not setup_environment():
        print("❌ Failed to set up environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup completed")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start Neo4j database (see README.md for instructions)")
    print("2. Edit .env file with your Neo4j settings")
    print("3. Test connection: poetry run python -m neo4j_learning.cli test")
    print("4. Run examples: poetry run python -m neo4j_learning.cli examples")


if __name__ == "__main__":
    main() 