# pwnelle

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

A modern binary analysis tool that helps identify vulnerabilities and generates exploit templates.

## Features

- **Binary Analysis**: Identifies protections, vulnerabilities, and executable properties
- **Vulnerability Detection**: Recognizes common vulnerability patterns in binaries
- **Template Generation**: Creates customized exploit templates based on detected vulnerabilities
- **ROP Gadget Identification**: Finds and catalogs useful code gadgets
- **Comprehensive Reporting**: Generates detailed HTML and JSON reports

## Installation

```bash
# Install from PyPI
pip install pwnelle

# Or install from source
git clone https://github.com/EllE961/pwnelle.git
cd pwnelle
pip install -e .
```

## Quick Start

```bash
# Basic analysis
pwnelle ./path/to/binary

# Generate exploit template
pwnelle ./path/to/binary --auto-exploit

# Save to specific directory
pwnelle ./path/to/binary -o output_dir
```

## Usage

```
usage: pwnelle <binary> [options]

positional arguments:
  binary               Path to the ELF binary to analyze

optional arguments:
  -h, --help           Show help message and exit
  -o, --output         Output directory (default: pwnelle-out/<binary_name>)
  -v, --verbose        Show progress bars, extra diagnostics
  --auto-exploit       Generate exploit template
  --depth INT          Nested decode depth for smart strings (default: 2)
  --max-length INT     Maximum suggested payload length for template (default: 2000)
```

## Output

pwnelle generates several files to assist with binary exploitation:

- `analysis.json`: Full analysis results
- `report.md`: Detailed vulnerability report
- `report.html`: Interactive HTML report
- `gadgets.py`: Detected ROP gadgets
- `exploit_template.py`: Customized exploit skeleton (when using --auto-exploit)

## Requirements

- Python 3.8+
- pwntools
- capstone
- pyelftools
- ROPgadget
- python-Levenshtein

## License

MIT
