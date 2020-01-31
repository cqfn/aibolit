import sys
import subprocess
import os
import uuid
import shutil
from bs4 import BeautifulSoup
import lxml

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CCMetric(object):
    """Main Cyclical Complexity class."""

    input = ''

    def __init__(self, input):
        """Initialize class."""
        super(CCMetric, self).__init__()
        if len(input) == 0:
            raise ValueError('Empty file for analysis')
        else:
            self.input = input

    def run(self, showoutput=False):
        """Run Cyclical Complexity analaysis"""
        root = uuid.uuid4().hex
        dirName = root + '/src/main/java'
        os.makedirs(dirName)
        try:
            if os.path.isdir(self.input):
                shutil.copytree(self.input, dirName + '/input.java')
            elif os.path.isfile(self.input):
                pos1 = self.input.rfind('/')
                os.makedirs(dirName + '/' + self.input[0:pos1])
                shutil.copyfile(self.input, os.path.join(dirName, self.input))
            else:
                self.finishAnalysis(root)
                return {'errors': [{'file': self.input, 'message': 'File does not exist'}]}
        except IOError:
            self.finishAnalysis(root)
            return {'errors': [{'file': self.input, 'message': 'File does not exist'}]}

        shutil.copyfile('pom.xml', root + '/pom.xml')
        shutil.copyfile('cyclical.xml', root + '/cyclical.xml')
        if showoutput:
            subprocess.run(['mvn', 'pmd:pmd'], cwd=root)
        else:
            subprocess.run(['mvn', 'pmd:pmd'], cwd=root,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

        f = open(root + '/target/pmd.xml', 'r')
        if f is not None:
            f.close()
            res = self.parseFile(root)
            self.finishAnalysis(root)
            return res
        else:
            self.finishAnalysis(root)
            return {'errors': [{'file': self.input, 'message': 'File analyze failed'}]}

    def parseFile(self, root):
        result = {'data': [], 'errors': []}
        content = []
        # Read the XML file
        with open(root + '/target/pmd.xml', 'r') as file:
            # Read each line in the file, readlines() returns a list of lines
            content = file.readlines()
            # Combine the lines in the list into a string
            content = "".join(content)
            soup = BeautifulSoup(content, 'lxml')
            files = soup.find_all("file")
            for file in files:
                out = file.violation.string
                name = file['name']
                pos1 = name.find(root + '/src/main/java/')
                pos1 = pos1 + len(root + '/src/main/java/')
                name = name[pos1:]
                pos1 = out.find('has a total cyclomatic complexity')
                pos1 = out.find('of ', pos1)
                pos1 = pos1 + 3
                pos2 = out.find('(', pos1)
                complexity = int(out[pos1:pos2-1])
                result['data'].append({'file': name, 'complexity': complexity})
            errors = soup.find_all("error")
            for error in errors:
                name = error['filename']
                pos1 = name.find(root + '/src/main/java/')
                pos1 = pos1 + len(root + '/src/main/java/')
                name = name[pos1:]
                result['errors'].append({'file': name, 'message': error['msg']})
        return result

    def finishAnalysis(self, root):
        """Finish anayze."""
        shutil.rmtree(root)
        pass


if __name__ == '__main__':
    metric = CCMetric(sys.argv[1])
    res = metric.run(showoutput=True)
    print('Received: ' + str(res))
    if len(res['errors']) > 0:
        print(f"{bcolors.FAIL}" + str(res['errors'][0]) + f"{bcolors.ENDC}")
    elif len(res['data']) > 0:
        if res['data'][0]['complexity'] <= 10:
            print(f"{bcolors.OKGREEN}Total cyclomatic complexity: " +
                  str(res['data'][0]['complexity']) + f"{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Total cyclomatic complexity: " +
                  str(res['data'][0]['complexity']) + f"{bcolors.ENDC}")
