#!/usr/bin/env python3
"""
Tests for the shared utility functions
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_example_contents, print_scan_result_summary, print_detection_summary


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""

    def test_get_example_contents(self):
        """Test that example contents are returned correctly"""
        contents = get_example_contents()
        self.assertIsInstance(contents, list)
        self.assertTrue(len(contents) > 0)
        self.assertIn("prompt", contents[0])
        self.assertIn("response", contents[0])

    @patch("builtins.print")
    def test_print_scan_result_summary(self, mock_print):
        """Test print_scan_result_summary function"""
        # Create mock scan response
        mock_response = MagicMock()
        mock_response.scan_id = "test-scan-id"
        mock_response.report_id = "test-report-id"
        mock_response.tr_id = "test-transaction-id"
        mock_response.category = "test-category"
        mock_response.action = "allow"
        
        # Mock detection objects
        mock_prompt_detected = MagicMock()
        mock_prompt_detected.url_cats = False
        mock_prompt_detected.dlp = False
        mock_prompt_detected.injection = False
        
        mock_response_detected = MagicMock()
        mock_response_detected.url_cats = False
        mock_response_detected.dlp = False
        
        mock_response.prompt_detected = mock_prompt_detected
        mock_response.response_detected = mock_response_detected
        
        # Call the function
        print_scan_result_summary(mock_response)
        
        # Verify print was called with expected arguments
        mock_print.assert_any_call("Scan ID: test-scan-id")
        mock_print.assert_any_call("Report ID: test-report-id")
        mock_print.assert_any_call("Transaction ID: test-transaction-id")
        mock_print.assert_any_call("Category: test-category")
        mock_print.assert_any_call("Action: allow")
        mock_print.assert_any_call("✅ Content allowed")

    @patch("builtins.print")
    def test_print_detection_summary_with_issues(self, mock_print):
        """Test print_detection_summary function with detected issues"""
        # Create mock detection with issues
        mock_detection = MagicMock()
        mock_detection.url_cats = True
        mock_detection.dlp = True
        mock_detection.injection = True
        
        # Call the function for prompt
        print_detection_summary("Prompt", mock_detection)
        
        # Verify print was called with expected arguments
        mock_print.assert_called_with("Prompt detected issues: URL categories, DLP, Injection")
        
        # Reset mock
        mock_print.reset_mock()
        
        # Call the function for response (should not include injection)
        print_detection_summary("Response", mock_detection)
        
        # Verify print was called with expected arguments
        mock_print.assert_called_with("Response detected issues: URL categories, DLP")


if __name__ == "__main__":
    unittest.main()