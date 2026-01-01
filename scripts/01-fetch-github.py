# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT


import argparse
import os
import subprocess

import requests as r
from bs4 import BeautifulSoup


def downloadrepos():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--nrepos', type=int, required=False, default=100)
    args = parser.parse_args()
    numrepos = args.nrepos
    repos = 'target/01'
    if not os.path.isdir(repos):
        os.makedirs(repos)
    result = r.get('https://github.com/trending/java?since=daily', timeout=30)
    soup = BeautifulSoup(result.text)
    for city in soup.find_all('h1', {'class': 'h3 lh-condensed'}):
        if numrepos <= 0:
            break
        numrepos = numrepos - 1
        path = city.a['href'].split('/')
        if not os.path.isdir(os.path.join(repos, path[len(path) - 2])):
            os.makedirs(os.path.join(repos, path[len(path) - 2]))
        if not os.path.isdir(os.path.join(repos, path[len(path) - 2], path[len(path) - 1])):
            subprocess.run(['git', 'clone', 'https://github.com' + city.a['href'] + '.git'],
                           cwd=os.path.join(repos, path[len(path) - 2]), check=False)


if __name__ == '__main__':
    downloadrepos()
