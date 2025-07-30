# Squad Builder SDK

A Python package that provides a unified interface for cloud storage operations across multiple providers.

## Features

- Unified interface for Amazon S3, Azure Blob Storage, and Google Cloud Storage
- Simple API for common operations: list files, download, upload, and stream
- Support for pre-signed URLs for secure storage access
- Robust XML and JSON response handling for different storage providers
- Environment-based storage path separation
- Configurable content types for file uploads

## Installation

```bash
# Install from PyPI
pip install squad-builder
```

## Usage

### Basic Usage

```python
import uuid
from squad_builder import DataClient

# Initialize with required parameters
client = DataClient(
    api_key="your_api_key",
    organization_id=uuid.UUID("550e8400-e29b-41d4-a716-446655440000"),
    environment="dev",  # Supports environments like "dev", "prod", etc.
    api_url="https://your-api.com"
)

# List files (optionally with a prefix)
files = client.list_files(prefix="images/")
for file in files:
    print(f"File: {file['key']}, Size: {file.get('size', 'Unknown')}")

# Download a file
# Note: No need to include environment in file path - it's handled by the API
client.download_file(
    file_path="report.pdf",
    destination="/local/path/report.pdf"
)

# Upload a file with custom content type
# Note: No need to include environment in file path - it's handled by the API
result = client.upload_file(
    file_path="report.pdf",
    file_obj="/local/path/report.pdf",  # Can be a path or a file-like object
    content_type="application/pdf"
)

# Stream a file (useful for large files or temporary access)
# Note: No need to include environment in file path - it's handled by the API
file_stream = client.stream_file("large_file.zip")
content = file_stream.read()
# Process the content as needed...
```

### Storage API Integration

The SDK communicates with a storage API that provides pre-signed URLs for various storage operations. The API handles authentication and storage provider configuration, while the SDK focuses on client-side operations.

The storage API should support the following endpoints:

- `GET /storage/list` - List files in storage
- `GET /storage/download` - Get a pre-signed URL for downloading files
- `GET /storage/upload` - Get a pre-signed URL for uploading files
- `GET /storage/stream` - Get a pre-signed URL for streaming files

Each endpoint accepts the following parameters:
- `organization_id` - UUID of the organization
- `environment` - Environment name (e.g., "dev", "prod")
- Other operation-specific parameters (file_path, content_type, etc.)

**Important**: The environment is automatically added as a prefix to your file paths by the server. For example, if your environment is "dev" and your file_path is "report.pdf", the actual path in storage will be "dev/report.pdf".

## Advanced Usage

### Handling Different Response Formats

The SDK automatically handles both JSON and XML response formats, making it compatible with various storage providers:

- Amazon S3 (typically returns XML)
- Azure Blob Storage
- Google Cloud Storage

### Working with Multiple Environments

The SDK supports environment-based path separation to keep development, testing, and production data isolated. The environment is specified when creating the client and is automatically applied to all operations:

```python
# For development
dev_client = DataClient(
    api_key="your_api_key",
    organization_id=your_org_id,
    environment="dev",
    api_url="https://your-api.com"
)

# For production
prod_client = DataClient(
    api_key="your_api_key",
    organization_id=your_org_id,
    environment="prod",
    api_url="https://your-api.com"
)

# Files will be automatically stored in separate paths:
# - dev/report.pdf
# - prod/report.pdf
```

## Complete Example

See the `examples/storage_client_example.py` file for a complete working example of all operations.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/squad-builder.git
cd squad-builder

# Install development dependencies
pip install -e .
pip install pytest pytest-cov black isort mypy
```

### Running Tests

```bash
pytest
```

## Publishing to PyPI

To publish the package to PyPI, follow these steps:

### Prerequisites

```bash
# Install publishing tools
pip install build twine
```

### Build the Package

```bash
# Build the distribution package
python -m build
```

This will create both a source distribution (.tar.gz) and a wheel (.whl) in the `dist/` directory.

### Upload to PyPI

```bash
# Upload to PyPI (you'll need a PyPI account)
twine upload dist/*
```

You'll be prompted for your PyPI username and password. For more secure authentication, you can create a PyPI API token and use it instead of your password.

### Upload to TestPyPI (Optional)

If you want to test the upload process before publishing to the main PyPI index:

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ squad-builder
```

## License

MIT