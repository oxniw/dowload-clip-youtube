# Description: start_server.py

## Overview
Coordinates Uvicorn server startup and launches the user's default web browser to the application URL.

## Exports & Functions
- `open_browser_delayed(url: str, delay_seconds: float = 1.0)`
  - **Description**: Background thread helper opening the web browser after Uvicorn initializes.
  - **Parameters**:
    - `url`: Target HTTP URL.
    - `delay_seconds`: Pause duration in seconds before opening.
- `start_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, auto_open: bool = True)`
  - **Description**: Instantiates the FastAPI application via `create_app` and runs the Uvicorn ASGI server.
  - **Parameters**:
    - `host`: Network interface binding.
    - `port`: Network port number.
    - `auto_open`: If `True`, launches default browser.

## Dependencies & Data Flow
- **Imports**: `threading`, `time`, `webbrowser`, `uvicorn`, `config`, `create_app`.
- **Invoked By**: `main.py`.
- **Data Flow**: CLI arguments -> `start_server` -> launches Uvicorn server process and browser.
