import javalang


class NCSSMetric():
    filename = ''

    def __init__(self, input):
        """Initialize class."""
        if len(filename) == 0:
            raise ValueError('Empty file for analysis')
        self.filename = filename
    
    def value(self):
        f = open(self.filename, "r")
        code = f.read()
        f.close()

        tokens = list(javalang.tokenizer.tokenize(code))
        tree = javalang.parse.parse(code)
        
        metric = 0
        for path, node in tree:
            node_type = str(type(node))
            if 'Statement' in node_type:
                metric += 1
            elif 'VariableDeclarator' == node_type:
                metric += 1
            elif 'Assignment' == node_type:
                metric += 1
            elif 'Declaration' in node_type and 'LocalVariableDeclaration' not in node_type \
                                            and 'PackageDeclaration' not in node_type:
                metric += 1
            
        return metric
