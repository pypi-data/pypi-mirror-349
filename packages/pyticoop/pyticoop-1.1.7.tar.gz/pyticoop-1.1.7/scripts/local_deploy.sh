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
    echo "  This script creates and pushes a git tag v<version>, builds the package,"
    echo "  and deploys it to PyPI. Requires TWINE_PASSWORD environment variable"
    echo "  to be set with your PyPI token."
    echo
    echo "Environment Variables:"
    echo "  TWINE_PASSWORD    PyPI token for authentication"
    echo
    echo "Example:"
    echo "  export TWINE_PASSWORD='your_pypi_token'"
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

# Check if TWINE_PASSWORD is set
if [ -z "$TWINE_PASSWORD" ]; then
    echo "Error: TWINE_PASSWORD environment variable not set"
    echo "Please set it with: export TWINE_PASSWORD='your_pypi_token'"
    exit 1
fi

echo "Creating and pushing tag $TAG..."
git tag "$TAG"
git push origin "$TAG"

echo "Checking out tag..."
git checkout "$TAG"

echo "Cleaning previous builds..."
rm -rf dist/

echo "Building package..."
CI_COMMIT_TAG="$TAG" ./scripts/build.sh

echo "Verifying built package..."
ls dist/

echo "Uploading to PyPI..."
python -m twine upload dist/* \
    --repository-url https://upload.pypi.org/legacy/ \
    --username __token__ \
    --password "$TWINE_PASSWORD"

echo "Returning to previous branch..."
git checkout -

echo "Deployment completed successfully!"