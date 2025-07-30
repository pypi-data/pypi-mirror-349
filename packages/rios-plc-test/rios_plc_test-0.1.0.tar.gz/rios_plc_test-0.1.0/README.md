# rios-plc-test

A simple command-line tool for testing PLC (Programmable Logic Controller) integrations, developed by RIOS. This tool is designed to help RIOS engineers and external vendors verify connectivity and tag reading with Allen-Bradley Logix PLCs using the `pycomm3` library.

## Features
- Connects to a specified PLC host
- Reads a specified tag in a loop
- Logs tag values and connection issues
- Automatic reconnection on communication errors

## Installation

### From PyPI (Recommended for Vendors)
```bash
pip install rios-plc-test
```

### From Source (For RIOS Developers)
Clone this repository and install in editable mode:
```bash
git clone <this-repo-url>
cd rios-plc-test
python3 -m venv .venv
.venv/bin/pip install -e .
```

## Usage

After installation, use the CLI tool to connect to a PLC and read a tag:

```bash
rios-plc-test <PLC_HOST> <TAG> [--log-level LOG_LEVEL]
```

- `<PLC_HOST>`: IP address or hostname of the PLC (e.g., `192.168.200.35`)
- `<TAG>`: The tag name to read (e.g., `jackladder_1_count_int32`)
- `--log-level`: (Optional) Set logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). Default is `INFO`.

### Example
```bash
rios-plc-test 192.168.200.35 jackladder_1_count_int32 --log-level DEBUG
```

The tool will continuously read the specified tag and log the results. If the connection is lost, it will attempt to reconnect every 5 seconds.

## Development
- Main entry point: `src/rios_plc_test/cli.py`
- Uses [`pycomm3`](https://github.com/ottowayi/pycomm3) for PLC communication
- To run locally: `make run HOST=1.2.3.4 TAG=foo` (see `Makefile` for details)

## Publishing
To publish a new version to PyPI:
```bash
make build
```

## Support & Contact
For questions, issues, or feature requests, please contact the RIOS engineering team or open an issue in this repository.

---
© RIOS. For internal and vendor integration testing use. 