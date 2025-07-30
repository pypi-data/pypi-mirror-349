# surfing-python

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyPI](https://img.shields.io/badge/pypi-surfing_python-blue)

A Python binding for the [surfing](https://github.com/victor-iyi/surfing) Rust crate - extract JSON from text streams.

## Description

`surfing-python` provides Python bindings for the Rust `surfing` library, allowing you to easily extract JSON objects from unstructured text. It's perfect for scenarios where you need to extract structured data from logs, text files, or other sources that may contain JSON mixed with other content.

## Installation

```
pip install surfing-python
```

## Usage

### Basic Example

```python
import surfing_python

# Extract JSON from a text string
text = 'some random text {"key": "value"} more random text'
json_str = surfing_python.extract_json_to_string(text)
print(json_str)  # Output: {"key": "value"}
```

### Error Handling

```python
import surfing_python

try:
    # No JSON in this string
    json_str = surfing_python.extract_json_to_string("no json here")
except ValueError as e:
    print(f"Error: {e}")  # Will print an error message
```

## Features

- Fast and efficient JSON extraction powered by Rust
- Simple Python API
- Detailed error messages
- Works with nested and complex JSON structures

## Development

### Prerequisites

- Python 3.8+
- Rust toolchain
- [maturin](https://github.com/PyO3/maturin) for building the package

### Building from source

1. Clone the repository
   ```
   git clone https://github.com/your-username/surfing-python.git
   cd surfing-python
   ```

2. Create and activate a virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies
   ```
   pip install maturin
   ```

4. Build and install in development mode
   ```
   maturin develop
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [surfing](https://github.com/victor-iyi/surfing) - The Rust library this package wraps
- [PyO3](https://github.com/PyO3/pyo3) - Rust bindings for Python
- [maturin](https://github.com/PyO3/maturin) - Build, package and upload Python extensions