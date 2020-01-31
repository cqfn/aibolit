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


root = uuid.uuid4().hex
dirName = root + '/src/main/java'
os.makedirs(dirName)
dest = shutil.copyfile(sys.argv[1], dirName + '/input.java')
dest = shutil.copyfile('pom.xml', root + '/pom.xml')
dest = shutil.copyfile('cyclical.xml', root + '/cyclical.xml')

result = subprocess.run(['mvn', 'pmd:pmd'], cwd=root,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

f = open(root + "/target/pmd.xml", "r")
if f is not None:
    out = f.read()
    pos1 = out.find('PMDException: Error while parsing')
    if pos1 >= 0:
        print(f"{bcolors.FAIL}Incorrect input file{bcolors.ENDC}")
    else:
        pos1 = out.find('has a total cyclomatic complexity')
        pos1 = out.find('of ', pos1)
        pos1 = pos1 + 3
        pos2 = out.find('(', pos1)

        complexity = int(out[pos1:pos2-1])
        if complexity <= 10:
            print(f"{bcolors.OKGREEN}Total cyclomatic complexity: " +
                  str(complexity) + f"{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Total cyclomatic complexity: " +
                  str(complexity) + f"{bcolors.ENDC}")
else:
    print(f"{bcolors.FAIL}File analyze failed{bcolors.ENDC}")
shutil.rmtree(root)
