To run:
1. Install java
2. Install Maven `sudo apt install maven`
3. Install Python 3.6 or higher
4. Install dependencies: `pip3 install -r requirements.txt`
5. Execute: `python3 run.py ../input/Complicated.java`, where:
  * first parameter is path to current folder run.py
  * second parameter is path to analyzed java file.

Usage:
```
from main import CCMetric
input = `myfile.java`
showlog = True
metric = CCMetric(input)
print(metric.value(showlog))
```
