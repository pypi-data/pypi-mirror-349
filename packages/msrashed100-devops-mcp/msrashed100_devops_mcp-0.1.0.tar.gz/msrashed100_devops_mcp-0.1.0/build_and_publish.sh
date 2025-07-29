#!/bin/bash
# Script to build and publish the DevOps MCP Server package

set -e  # Exit on error

echo "DevOps MCP Server - Build and Publish"
echo "===================================="
echo

# Check if Python 3.12+ is installed
python_version=$(python --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 12 ]); then
    echo "Error: Python 3.12 or higher is required."
    echo "Current version: $python_version"
    echo "Please install Python 3.12+ and try again."
    exit 1
fi

echo "Python version $python_version detected."
echo

# Check if build tools are installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed."
    echo "Please install uv and try again."
    echo "You can install uv with: pip install uv"
    exit 1
fi

if ! command -v build &> /dev/null; then
    echo "Installing build package..."
    uv pip install build
fi

if ! command -v twine &> /dev/null; then
    echo "Installing twine package..."
    uv pip install twine
fi

echo "Build tools detected."
echo

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/
echo "Previous builds cleaned."
echo

# Build the package
echo "Building the package..."
python -m build
echo "Package built successfully."
echo

# List the built files
echo "Built files:"
ls -l dist/
echo

# Ask if the user wants to publish to PyPI
read -p "Do you want to publish to PyPI? (y/n): " publish_choice

if [[ $publish_choice == "y" || $publish_choice == "Y" ]]; then
    # Check if the user is logged in to PyPI
    if ! twine check dist/*; then
        echo "Error: Package check failed."
        exit 1
    fi
    
    # Ask if the user wants to publish to TestPyPI first
    read -p "Do you want to publish to TestPyPI first? (y/n): " testpypi_choice
    
    if [[ $testpypi_choice == "y" || $testpypi_choice == "Y" ]]; then
        echo "Publishing to TestPyPI..."
        twine upload --repository testpypi dist/*
        echo "Package published to TestPyPI."
        echo
        echo "You can install it with:"
        echo "uv pip install --index-url https://test.pypi.org/simple/ devops-mcp-server"
        echo
    fi
    
    # Ask if the user wants to publish to PyPI
    read -p "Do you want to publish to PyPI? (y/n): " pypi_choice
    
    if [[ $pypi_choice == "y" || $pypi_choice == "Y" ]]; then
        echo "Publishing to PyPI..."
        twine upload dist/*
        echo "Package published to PyPI."
        echo
        echo "You can install it with:"
        echo "uv pip install devops-mcp-server"
        echo
    fi
else
    echo "Package not published."
    echo
    echo "To publish manually, run:"
    echo "twine upload dist/*"
    echo
fi

echo "Build and publish process completed."
echo
echo "Installation instructions:"
echo "1. Using uv: uv pip install devops-mcp-server"
echo "2. Using uvx: uvx devops-mcp-server"
echo