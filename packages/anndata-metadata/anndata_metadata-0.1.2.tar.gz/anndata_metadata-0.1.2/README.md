# anndata-metadata

**anndata-metadata** is a Python library and CLI tool for extracting metadata from [AnnData](https://anndata.readthedocs.io/) `.h5ad` files, both locally and on S3. When extracting metadata from S3, it uses partial downloads to dramatically speed up extraction.

It provides utilities to summarize cell, gene, and matrix information, and supports batch processing of directories.

It can create a `.parquet` index of the metadata for all of the files in a directory (S3 or local).

## Library Overview

The core library is in `src/anndata_metadata/` and provides:

- **Metadata extraction**: Functions to extract key metadata (cell count, gene count, matrix format, group contents, etc.) from AnnData `.h5ad` files.
- **S3 and local support**: Utilities to process files both on local disk and in S3 buckets.
- **JSON-serializable output**: All metadata is returned as Python dictionaries with native types.

## Installing

```
pip install anndata-metadata
```

## CLI Usage

**Usage:**
```sh
usage: anndata-metadata [-h] [-o OBS] [-c COUNT] input_path output

Extract AnnData metadata from file(s) or S3 object(s).

positional arguments:
  input_path            Input file, directory, S3 URI, or S3 directory URI
  output                Output filename (JSON for single file, Parquet for directory,
                        '-' for stdout)

options:
  -h, --help            show this help message and exit
  -o OBS, --obs OBS     Observation column to count (can be specified multiple times)
  -c COUNT, --count COUNT
                        Maximum number of files to process (for directories/S3
                        directories)
```

**Examples:**
```sh
anndata-metadata data/myfile.h5ad metadata.json
anndata-metadata data/ metadata.parquet
anndata-metadata s3://my-bucket/ metadata.parquet
```


## Development

### Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast Python environment management.

1. **Install dependencies:**
   ```sh
   uv sync # this gets the dependenceis you need to run the command
   uv sync --group dev # this gets the dev dependencies for testing and formatting
   ```

2. **Run tests:**
   ```sh
   uv run pytest
   ```

3. **Format code:**
   ```sh
   uv run yapf --recursive . --in-place
   ```

4. **Type check (mypy):**
   ```sh
   uv run mypy
   ```

5. **Run CLI**
   ```sh
   PYTHONPATH=src uv run python -m anndata_metadata
   ```

6. Build and test the wheel
   ```sh
   uv run python -m build
   ```
   and test it using
   ```sh
    python -m venv testenv
    source testenv/bin/activate
    pip install dist/anndata_metadata-*.whl --force-reinstall   
   ```
   you will now be able to run the cli command like this
   ```
    anndata-metadata
   ```


### Project Structure
```
.
├── src/
│ └── anndata_metadata/
│   ├── extract.py # Core metadata extraction logic
│   └── main.py # CLI entry point
├── test/ # Unit tests for extraction functions and CLI
├── README.md # Project documentation
└── pyproject.toml # Project metadata and dependencies
```

# TODO

- [x] add mypy support
- [x] add a wheel and submit to pypy
- [ ] CI/CD pipeline for updating pyp
- [ ] write partial results and skip previously written values