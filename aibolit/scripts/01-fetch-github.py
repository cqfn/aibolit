import subprocess
import os
import requests as r
from bs4 import BeautifulSoup

if not os.path.isdir('01/repos'):
    os.makedirs('01/repos')
f = open('01/found-java-files.txt', 'w+')
f.close()
r = r.get('https://github.com/trending/java?since=daily')
soup = BeautifulSoup(r.text)
for city in soup.find_all('h1', {'class': 'h3 lh-condensed'}):
    path = city.a['href'].split('/')
    if not os.path.isdir(os.path.join('01/repos', path[len(path) - 2])):
        os.makedirs(os.path.join('01/repos', path[len(path) - 2]))

    if not os.path.isdir(os.path.join('01/repos', path[len(path) - 2], path[len(path) - 1])):
        result = subprocess.run(['git', 'clone', 'https://github.com' + city.a['href'] + '.git'],
                                cwd=os.path.join('01/repos', path[len(path) - 2]))
    for root, dirs, files in os.walk(os.path.join('01/repos', path[len(path) - 2], path[len(path) - 1])):
        for file in files:
            if file[-5:] == ".java":
                count = 0
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        count += 1
                    if count > 50 and count < 300:
                        s = str(os.path.join(root, file))
                        f = open('01/found-java-files.txt', 'a')
                        f.write(s + '\n')
                        f.close()
