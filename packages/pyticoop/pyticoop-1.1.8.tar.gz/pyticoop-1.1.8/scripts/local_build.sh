#!/bin/bash
set -e  # Exit on error

usage() {
    echo "Usage: $0 [OPTIONS] <version>"
    echo
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo
    echo "Arguments:"
    echo "  version       Version number (e.g., 1.1.6)"
    echo
    echo "Description:"
    echo "  This script creates a git tag v<version> and builds the package"
    echo "  without pushing to remote or deploying to PyPI."
    echo
    echo "Example:"
    echo "  $0 1.1.6"
    exit 1
}

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        *) VERSION=$1; shift ;;
    esac
done

# Check if version argument is provided
if [ -z "$VERSION" ]; then
    usage
fi

TAG="v$VERSION"

echo "Creating tag $TAG..."
git tag "$TAG"

echo "Checking out tag..."
git checkout "$TAG"

echo "Cleaning previous builds..."
rm -rf dist/

echo "Building package..."
CI_COMMIT_TAG="$TAG" ./scripts/build.sh

echo "Built package:"
ls dist/

echo "Returning to previous branch..."
git checkout -

echo "Build completed successfully!"
echo "To deploy, run: ./scripts/local_deploy.sh $VERSION"