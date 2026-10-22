# Description: test_logic.py

## Overview
Unit test suite verifying domain logic: URL sanitization against SSRF and private networks, timestamp parsing across formats, and time boundary constraints.

## Exports & Functions
- `class TestDownloaderLogic(unittest.TestCase)`:
  - `test_url_validation_valid()`: Asserts valid YouTube URLs succeed.
  - `test_url_validation_invalid()`: Asserts private IP ranges, loopback addresses, and unauthorized schemes are rejected with `ValueError`.
  - `test_time_to_seconds()`: Asserts string parsing into float seconds.
  - `test_parse_time_range()`: Asserts chronological boundaries and maximum clipping constraints.

## Dependencies & Data Flow
- **Imports**: `unittest`, `validate_url`, `parse_time_range`.
- **Invoked By**: `python test_logic.py`.
