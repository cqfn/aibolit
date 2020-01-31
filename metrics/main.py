import sys
import subprocess
import os
import uuid
import shutil


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
            shutil.copyfile(self.input, dirName + '/input.java')
        except IOError:
            self.finishAnalysis(root)
            return {'error': 'File ' + self.input + ' does not exist'}

        shutil.copyfile('pom.xml', root + '/pom.xml')
        shutil.copyfile('cyclical.xml', root + '/cyclical.xml')
        if showoutput:
            subprocess.run(['mvn', 'pmd:pmd'], cwd=root)
        else:
            subprocess.run(['mvn', 'pmd:pmd'], cwd=root,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

        f = open(root + "/target/pmd.xml", "r")
        if f is not None:
            out = f.read()
            pos1 = out.find('PMDException: Error while parsing')
            if pos1 >= 0:
                self.finishAnalysis(root)
                return {'error': 'Incorrect input file'}
            else:
                pos1 = out.find('has a total cyclomatic complexity')
                pos1 = out.find('of ', pos1)
                pos1 = pos1 + 3
                pos2 = out.find('(', pos1)
                self.finishAnalysis(root)
                return {'data': int(out[pos1:pos2-1])}
        else:
            self.finishAnalysis(root)
            return {'error': 'File analyze failed'}

    def finishAnalysis(self, root):
        """Finish anayze."""
        shutil.rmtree(root)


if __name__ == '__main__':
    metric = CCMetric(sys.argv[1])
    res = metric.run(showoutput=True)
    if 'error' in res:
        print(f"{bcolors.FAIL}" + res['error'] + f"{bcolors.ENDC}")
    elif res['data'] <= 10:
        print(f"{bcolors.OKGREEN}Total cyclomatic complexity: " +
              str(res['data']) + f"{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}Total cyclomatic complexity: " +
              str(res['data']) + f"{bcolors.ENDC}")
