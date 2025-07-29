#!/bin/bash
set -e  # Exit on error

# Function to update version in pyproject.toml
update_version() {
    local version=$1
    version=${version#v}  # Remove 'v' prefix
    echo "Updating version to $version in pyproject.toml"
    sed -i "s/version = .*/version = \"$version\"/" pyproject.toml
}

# Function to build package
build_package() {
    echo "Installing build dependencies..."
    pip install --upgrade pip setuptools wheel build

    echo "Building package..."
    python -m build
}

main() {
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    # If we have a tag, use it for versioning
    if [ -n "$CI_COMMIT_TAG" ]; then
        update_version "$CI_COMMIT_TAG"
    fi

    # Build package
    build_package

    echo "Build completed successfully"
}

main "$@"