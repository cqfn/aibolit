import re


class RemoveComments:

    def __init__(self):
        pass

    @staticmethod
    def remove_comments(string):
        # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "",
                        string)
        # remove all occurrence single-line comments (//COMMENT\n ) from string
        string = re.sub(re.compile(r"//.*?\n"), "",
                        string)
        return string
