# Description: main.py

## Overview
Application entry point that parses command-line arguments and invokes server startup.

## Exports & Functions
- `main()`
  - **Description**: Configures `argparse` with `--host`, `--port`, and `--no-browser` options, then delegates execution to `start_server()`.
  - **Parameters**: None.
  - **Returns**: None.

## Dependencies & Data Flow
- **Imports**: `argparse`, `config`, `start_server.start_server`.
- **Invoked By**: Direct terminal execution (`python main.py`).
- **Data Flow**: Command line options -> argument parser -> `start_server()`.
