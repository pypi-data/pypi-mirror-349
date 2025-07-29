#!/bin/bash
set -e  # Exit on error

# Function to check for built package
check_dist() {
    if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
        echo "Error: No distribution files found in dist directory"
        exit 1
    fi
}

# Function to upload to PyPI
upload_to_pypi() {
    if [ -z "$TWINE_PASSWORD" ]; then
        echo "Error: TWINE_PASSWORD environment variable not set"
        exit 1
    fi

    echo "Installing twine..."
    pip install --upgrade twine

    echo "Uploading to PyPI..."
    python -m twine upload dist/* \
        --repository-url https://upload.pypi.org/legacy/ \
        --username __token__ \
        --password "$TWINE_PASSWORD"
}

main() {
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi

    # Check for built package
    check_dist

    # Upload to PyPI
    upload_to_pypi

    echo "Deployment completed successfully"
}

main "$@"