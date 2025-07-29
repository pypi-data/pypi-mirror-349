#!/bin/bash
# Script to build and publish the DevOps MCP Server package with version incrementing

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

# Function to extract current version from pyproject.toml
get_current_version() {
    grep -E "^version = \"[0-9]+\.[0-9]+\.[0-9]+\"" pyproject.toml | cut -d'"' -f2
}

# Function to increment version
increment_version() {
    local version=$1
    local increment_type=$2
    
    # Split version into major, minor, patch
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    local patch=$(echo $version | cut -d. -f3)
    
    # Increment based on type
    case $increment_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo "Invalid increment type. Using patch."
            patch=$((patch + 1))
            ;;
    esac
    
    echo "$major.$minor.$patch"
}

# Function to update version in pyproject.toml
update_version() {
    local old_version=$1
    local new_version=$2
    
    # Use sed to replace the version in pyproject.toml
    sed -i "s/version = \"$old_version\"/version = \"$new_version\"/" pyproject.toml
    
    echo "Version updated from $old_version to $new_version in pyproject.toml"
}

# Get current version
current_version=$(get_current_version)
echo "Current version: $current_version"

# Ask for version increment type
echo "Version increment types:"
echo "1. Major (x.0.0) - For incompatible API changes"
echo "2. Minor (0.x.0) - For new functionality in a backward compatible manner"
echo "3. Patch (0.0.x) - For backward compatible bug fixes"
read -p "Choose version increment type (1-3) [default: 3]: " increment_choice

case $increment_choice in
    1) increment_type="major" ;;
    2) increment_type="minor" ;;
    *) increment_type="patch" ;;
esac

# Increment version
new_version=$(increment_version $current_version $increment_type)
echo "New version will be: $new_version"
read -p "Proceed with this version? (y/n) [default: y]: " version_confirm

if [[ $version_confirm == "n" || $version_confirm == "N" ]]; then
    echo "Version update cancelled."
    exit 0
fi

# Update version in pyproject.toml
update_version $current_version $new_version

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/
echo "Previous builds cleaned."
echo

# Build the package
echo "Building the package version $new_version..."
python -m build
echo "Package built successfully."
echo

# List the built files
echo "Built files:"
ls -l dist/
echo

# Get package name from pyproject.toml
package_name=$(grep -E "^name = \"[^\"]+\"" pyproject.toml | cut -d'"' -f2)
echo "Package name: $package_name"
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
        echo "uv pip install --index-url https://test.pypi.org/simple/ $package_name"
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
        echo "uv pip install $package_name"
        echo
    fi
else
    echo "Package not published."
    echo
    echo "To publish manually, run:"
    echo "twine upload dist/*"
    echo
fi

# Create git tag for the new version
read -p "Do you want to create a git tag for version $new_version? (y/n): " tag_choice

if [[ $tag_choice == "y" || $tag_choice == "Y" ]]; then
    echo "Creating git tag v$new_version..."
    git add pyproject.toml
    git commit -m "Bump version to $new_version"
    git tag -a "v$new_version" -m "Version $new_version"
    
    read -p "Do you want to push the tag to remote repository? (y/n): " push_choice
    if [[ $push_choice == "y" || $push_choice == "Y" ]]; then
        git push origin "v$new_version"
        echo "Tag pushed to remote repository."
    else
        echo "Tag created locally. Use 'git push origin v$new_version' to push it to remote."
    fi
fi

echo "Build and publish process completed."
echo
echo "Installation instructions:"
echo "1. Using uv: uv pip install $package_name"
echo "2. Using uvx: uvx $package_name"
echo