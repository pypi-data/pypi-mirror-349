# chunkrs

A high-performance parallel file downloader with Python bindings, powered by Rust.

## Installation

```bash
pip install chunkrs
```

CLI also available with:
```bash
uvx chunkrs --help

uvx tool install chunkrs
chunkrs --help
```

## Usage

```python
from chunkrs import download

# Basic usage
download(url="https://example.com/large-file.zip", output_file="large-file.zip")

# Advanced usage
download(
    url="https://example.com/large-file.zip",
    output_file="large-file.zip",
    chunk_size=16 * 1024 * 1024,  # 16MB chunks
    max_parallel=8,               # Limit parallel connections
    verbose=False                 # Hide progress bars
)
```

## Features

- Multi-threaded parallel downloads
- Configurable chunk size and connection limits
- Progress tracking with statistics
- Pre-allocation of file space for performance

## License

MIT
