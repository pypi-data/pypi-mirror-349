import unittest
from unittest.mock import patch
import argparse
from io import StringIO
import sys

from trail.main import parse_arguments
from trail.exception.trail import RemoteTrailException


class TestCLI(unittest.TestCase):
    def setUp(self):
        # Mock config_utils functions
        self.patcher_set_project = patch("trail.main.set_project")
        self.mock_set_project = self.patcher_set_project.start()
        self.mock_set_project.return_value = "test_project"

        self.patcher_set_experiment = patch("trail.main.set_experiment")
        self.mock_set_experiment = self.patcher_set_experiment.start()
        self.mock_set_experiment.return_value = "test_experiment"

        # Capture stdout for testing print statements
        self.stdout_patcher = patch("sys.stdout", new_callable=StringIO)
        self.mock_stdout = self.stdout_patcher.start()

    def tearDown(self):
        self.patcher_set_project.stop()
        self.patcher_set_experiment.stop()
        self.stdout_patcher.stop()

    def test_cli_set_project_direct(self):
        """Test setting project via CLI with direct ID"""
        test_args = ["trail", "--set-project", "test_project"]
        with patch("sys.argv", test_args):
            parse_arguments()

        self.mock_set_project.assert_called_with("test_project", interactive=False)
        self.assertIn("Project ID set to: test_project", self.mock_stdout.getvalue())

    def test_cli_set_project_interactive(self):
        """Test setting project via CLI interactively"""
        test_args = ["trail", "--set-project", "select"]
        with patch("sys.argv", test_args):
            parse_arguments()

        self.mock_set_project.assert_called_with(None, interactive=True)
        self.assertIn("Project ID set to: test_project", self.mock_stdout.getvalue())

    def test_cli_set_experiment_direct(self):
        """Test setting experiment via CLI with direct ID"""
        test_args = ["trail", "--set-experiment", "test_experiment"]
        with patch("sys.argv", test_args):
            parse_arguments()

        self.mock_set_experiment.assert_called_with(
            "test_experiment", interactive=False
        )
        self.assertIn(
            "Experiment ID set to: test_experiment", self.mock_stdout.getvalue()
        )

    def test_cli_set_experiment_interactive(self):
        """Test setting experiment via CLI interactively"""
        test_args = ["trail", "--set-experiment", "select"]
        with patch("sys.argv", test_args):
            parse_arguments()

        self.mock_set_experiment.assert_called_with(None, interactive=True)
        self.assertIn(
            "Experiment ID set to: test_experiment", self.mock_stdout.getvalue()
        )

    def test_cli_error_handling(self):
        """Test CLI error handling"""
        self.mock_set_project.side_effect = RemoteTrailException("Test error")

        test_args = ["trail", "--set-project", "test_project"]
        with patch("sys.argv", test_args):
            parse_arguments()

        self.assertIn("Test error", self.mock_stdout.getvalue())

    @patch("trail.main.uploads.upload_folder")
    def test_cli_upload_folder(self, mock_upload_folder):
        """Test uploading folder via CLI"""
        test_args = ["trail", "--upload-folder", "test_folder"]
        with patch("sys.argv", test_args):
            parse_arguments()

        mock_upload_folder.assert_called_with("test_folder")

    @patch("trail.main.add_test_results")
    def test_cli_add_pytest_results(self, mock_add_test_results):
        """Test adding pytest results via CLI"""
        test_args = ["trail", "--add-pytest-results", "test_results.xml"]
        with patch("sys.argv", test_args):
            parse_arguments()

        mock_add_test_results.assert_called_with("test_results.xml")
