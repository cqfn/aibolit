# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import subprocess
import os
import requests as r
from bs4 import BeautifulSoup
import argparse


def downloadrepos():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--repos', type=int, required=False, default=100)
    args = parser.parse_args()
    repos = args.repos
    repos = 'target/01'
    if not os.path.isdir(repos):
        os.makedirs(repos)
    r = r.get('https://github.com/trending/java?since=daily')
    soup = BeautifulSoup(r.text)
    for city in soup.find_all('h1', {'class': 'h3 lh-condensed'}):
        path = city.a['href'].split('/')
        if not os.path.isdir(os.path.join(repos, path[len(path) - 2])):
            os.makedirs(os.path.join(repos, path[len(path) - 2]))
        if not os.path.isdir(os.path.join(repos, path[len(path) - 2], path[len(path) - 1])):
            result = subprocess.run(['git', 'clone', 'https://github.com' + city.a['href'] + '.git'],
                                    cwd=os.path.join(repos, path[len(path) - 2]))


if __name__ == "__main__":
    downloadrepos()
