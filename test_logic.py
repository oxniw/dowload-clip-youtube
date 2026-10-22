# ==============================================================================
# File: .//Description-of-file/test_logic.md
# Overview: Unit tests for URL validation and timestamp parsing.
# ==============================================================================

import unittest
from validate_url import validate_url
from parse_time_range import parse_time_range, time_to_seconds

class TestDownloaderLogic(unittest.TestCase):
    def test_url_validation_valid(self):
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        ]
        for u in urls:
            self.assertEqual(validate_url(u), u)

    def test_url_validation_invalid(self):
        invalid_urls = [
            "http://localhost:8000/evil",
            "http://127.0.0.1/test",
            "https://169.254.169.254/latest/meta-data/",
            "file:///etc/passwd",
            "https://attacker.com/video.mp4",
        ]
        for u in invalid_urls:
            with self.assertRaises(ValueError):
                validate_url(u)

    def test_time_to_seconds(self):
        self.assertEqual(time_to_seconds("01:30"), 90.0)
        self.assertEqual(time_to_seconds("01:00:15"), 3615.0)
        self.assertEqual(time_to_seconds("45"), 45.0)
        self.assertIsNone(time_to_seconds(""))
        self.assertIsNone(time_to_seconds(None))

    def test_parse_time_range(self):
        start, end = parse_time_range("00:10", "01:00", total_duration=120)
        self.assertEqual(start, 10.0)
        self.assertEqual(end, 60.0)

        # End before start
        with self.assertRaises(ValueError):
            parse_time_range("01:00", "00:10")

        # Exceeds max duration
        with self.assertRaises(ValueError):
            parse_time_range("00:00", "03:00:00")

if __name__ == "__main__":
    unittest.main()
