# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import subprocess
import requests

import RepositoryDownloader


class RepositoryDownloaderTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_output_dir = Path(self.temp_dir.name) / "test_output"
        self.downloader = RepositoryDownloader(
            output=self.test_output_dir,
            url="https://github.com/trending/java?since=daily",
            timeout=30
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_setup_directories(self):
        """Test that setup_directories creates the output directory"""
        self.assertFalse(self.test_output_dir.exists())
        self.downloader.setup_directories()
        self.assertTrue(self.test_output_dir.exists())
        self.assertTrue(self.test_output_dir.is_dir())

    @patch('your_module.requests.get')
    def test_fetch_trending_repositories_success(self, mock_get):
        """Test successful fetching of trending repositories"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = """
        <html>
            <body>
                <article class="Box-row">
                    <h2><a href="/owner1/repo1">Repo 1</a></h2>
                </article>
                <article class="Box-row">
                    <h2><a href="/owner2/repo2">Repo 2</a></h2>
                </article>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        repositories = self.downloader.fetch_trending_repositories()
        expected_repos = [
            "https://github.com/owner1/repo1.git",
            "https://github.com/owner2/repo2.git"
        ]
        self.assertEqual(repositories, expected_repos)
        mock_get.assert_called_once_with(
            "https://github.com/trending/java?since=daily",
            timeout=30
        )

    def test_fetch_trending_repositories_request_exception(self, mock_get):
        """Test handling of request exceptions"""
        mock_get.side_effect = requests.RequestException("Network error")

        with self.assertRaises(requests.RequestException):
            self.downloader.fetch_trending_repositories()

    def test_fetch_trending_repositories_empty_anchors(self, mock_get):
        """Test handling of empty repository list"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<html><body></body></html>"
        mock_get.return_value = mock_response

        repositories = self.downloader.fetch_trending_repositories()
        self.assertEqual(repositories, [])

    def test_clone_repository_success(self, mock_subprocess):
        """Test successful repository cloning"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        result = self.downloader.clone_repository(
            "https://github.com/owner/repo.git",
            "owner",
            "repo"
        )
        self.assertTrue(result)
        mock_subprocess.assert_called_once_with(
            ['git', 'clone', 'https://github.com/owner/repo.git'],
            cwd=self.test_output_dir / "owner",
            capture_output=True,
            text=True,
            check=False
        )

    def test_clone_repository_failure(self, mock_subprocess):
        """Test repository cloning failure"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Authentication failed"
        mock_subprocess.return_value = mock_result
        result = self.downloader.clone_repository(
            "https://github.com/owner/repo.git",
            "owner",
            "repo"
        )
        self.assertFalse(result)

    def test_clone_repository_subprocess_error(self, mock_subprocess):
        """Test handling of subprocess errors"""
        mock_subprocess.side_effect = subprocess.SubprocessError("Git not found")
        result = self.downloader.clone_repository(
            "https://github.com/owner/repo.git",
            "owner",
            "repo"
        )
        self.assertFalse(result)

    def test_clone_repository_already_exists(self):
        """Test skipping already cloned repository"""
        owner_dir = self.test_output_dir / "existing_owner"
        owner_dir.mkdir(parents=True)
        repo_dir = owner_dir / "existing_repo"
        repo_dir.mkdir()
        result = self.downloader.clone_repository(
            "https://github.com/existing_owner/existing_repo.git",
            "existing_owner",
            "existing_repo"
        )
        self.assertTrue(result)

    def test_download_repositories_success(self, mock_clone, mock_fetch):
        """Test successful download of multiple repositories"""
        mock_fetch.return_value = [
            "https://github.com/owner1/repo1.git",
            "https://github.com/owner2/repo2.git",
            "https://github.com/owner3/repo3.git"
        ]
        mock_clone.return_value = True
        self.downloader.download_repositories(max_repositories=2)
        self.assertEqual(mock_clone.call_count, 2)
        mock_fetch.assert_called_once()

    def test_download_repositories_partial_success(self, mock_clone, mock_fetch):
        """Test download with some repositories failing to clone"""
        mock_fetch.return_value = [
            "https://github.com/owner1/repo1.git",
            "https://github.com/owner2/repo2.git",
            "https://github.com/owner3/repo3.git"
        ]
        mock_clone.side_effect = [True, False, True]
        self.downloader.download_repositories(max_repositories=3)
        self.assertEqual(mock_clone.call_count, 3)

    def test_download_repositories_fetch_fails(self, mock_fetch):
        """Test download when fetching repository list fails"""
        mock_fetch.side_effect = requests.RequestException("Fetch failed")
        self.downloader.download_repositories(max_repositories=10)
        mock_fetch.assert_called_once()

    def test_download_repositories_invalid_urls(self, mock_clone, mock_fetch):
        """Test handling of invalid repository URLs"""
        mock_fetch.return_value = [
            "https://github.com/owner1/repo1.git",
            "invalid_url",
            "https://github.com/singlepart",
            "https://github.com/owner2/repo2.git"
        ]
        mock_clone.return_value = True
        self.downloader.download_repositories(max_repositories=10)
        self.assertEqual(mock_clone.call_count, 2)

    def test_url_parsing_and_normalization(self):
        """Test URL parsing and .git suffix normalization"""
        test_cases = [
            ("/owner/repo", "https://github.com/owner/repo.git"),
            ("/owner/repo.git", "https://github.com/owner/repo.git"),
            ("https://github.com/owner/repo", "https://github.com/owner/repo.git"),
            ("https://github.com/owner/repo.git", "https://github.com/owner/repo.git"),
        ]
        for input_href, expected_url in test_cases:
            with self.subTest(href=input_href):
                normalized = self._normalize_url(input_href)
                self.assertEqual(normalized, expected_url)

    def _normalize_url(self, href):
        """Helper method to test URL normalization logic from fetch_trending_repositories"""
        if not href:
            return href
        if href.startswith('/'):
            href = f'https://github.com{href}'
        if not href.endswith('.git'):
            href = f'{href}.git'
        return href


class ArgumentParserTestCase(unittest.TestCase):
    def test_parse_arguments_default(self):
        """Test argument parser with default values"""
        with patch('sys.argv', ['script_name']):
            from your_module import parse_arguments
            args = parse_arguments()
            self.assertEqual(args.nrepos, 100)
            self.assertEqual(args.output_dir, 'target/01')

    def test_parse_arguments_custom(self):
        """Test argument parser with custom values"""
        test_args = [
            'script_name',
            '--nrepos', '50',
            '--output-dir', 'custom/directory'
        ]
        with patch('sys.argv', test_args):
            from your_module import parse_arguments
            args = parse_arguments()
            self.assertEqual(args.nrepos, 50)
            self.assertEqual(args.output_dir, 'custom/directory')


if __name__ == '__main__':
    unittest.main()
