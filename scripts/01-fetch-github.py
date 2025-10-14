# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup


class RepositoryDownloader:
    def __init__(self, output_dir: str = 'target/01', trend_url, timeout):
        self.output_dir = Path(output_dir)
        self.trending_url = trend_url
        self.request_timeout = timeout

    def setup_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_trending_repositories(self) -> List[str]:
        try:
            response = requests.get(self.trending_url, timeout=self.request_timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f'Error fetching trending repositories: {e}', file=sys.stderr)
            raise
        soup = BeautifulSoup(response.text, 'html.parser')
        repositories: List[str] = []
        anchors = (
            soup.select('article.Box-row h2 a[href]') or
            soup.select('h2.h3.lh-condensed a[href]') or
            soup.select('h1.h3.lh-condensed a[href]')
        )
        for a in anchors:
            href = (a.get('href') or '').strip()
            if not href:
                continue
            if href.startswith('/'):
                href = f'https://github.com{href}'
            if not href.endswith('.git'):
                href = f'{href}.git'
            repositories.append(href)
        return repositories

    def clone_repository(self, repo_url: str, owner: str, repo_name: str) -> bool:
        owner_dir = self.output_dir / owner
        owner_dir.mkdir(exist_ok=True)
        if (owner_dir / repo_name).exists():
            print(f'Repository {owner}/{repo_name} already exists, skipping...')
            return True
        try:
            result = subprocess.run(
                ['git', 'clone', repo_url],
                cwd=owner_dir,
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                print(f'Successfully cloned {owner}/{repo_name}')
                return True
            else:
                print(f'Failed to clone {owner}/{repo_name}: {result.stderr}')
                return False
        except subprocess.SubprocessError as e:
            print(f'Error cloning {owner}/{repo_name}: {e}', file=sys.stderr)
            return False

    def download_repositories(self, max_repositories: int) -> None:
        print(f'Fetching {max_repositories} trending Java repositories...')
        try:
            repositories = self.fetch_trending_repositories()
        except requests.RequestException:
            print('Failed to fetch repository list. Exiting.')
            return
        downloaded_count = 0
        for repo_url in repositories:
            if downloaded_count >= max_repositories:
                break
            path_parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
            if len(path_parts) < 2:
                continue
            owner, repo_name = path_parts[0], path_parts[1]
            print(f'Processing {owner}/{repo_name}...')
            if self.clone_repository(repo_url, owner, repo_name):
                downloaded_count += 1
        print(f'Downloaded {downloaded_count} repositories to {self.output_dir}')


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Download trending Java repositories from GitHub',
        add_help=True
    )
    parser.add_argument(
        '--nrepos',
        type=int,
        required=False,
        default=100,
        help='Number of repositories to download (default: 100)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        required=False,
        default='target/01',
        help='Output directory for downloaded repositories (default: target/01)'
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    downloader = RepositoryDownloader(args.output_dir, 'https://github.com/trending/java?since=daily', 30)
    downloader.setup_directories()
    downloader.download_repositories(args.nrepos)


if __name__ == '__main__':
    main()
