import subprocess
import os
import requests as r
from bs4 import BeautifulSoup


if not os.path.isdir("output"):
    os.mkdir('output')
r = r.get('https://github.com/trending/java?since=daily')
soup = BeautifulSoup(r.text)
for city in soup.find_all('h1', {'class': 'h3 lh-condensed'}):
    path = city.a['href'].split('/')
    if not os.path.isdir(os.path.join('output', path[len(path) - 1])):
        result = subprocess.run(['git', 'clone', 'https://github.com' + city.a['href'] + '.git'], cwd='output')
    for root, dirs, files in os.walk(os.path.join('output', path[len(path) - 1])):
        for file in files:
            if file[-5:] == ".java":
                count = 0
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        count += 1
                    if count > 50 and count < 300:
                        print(os.path.join(root, file))
