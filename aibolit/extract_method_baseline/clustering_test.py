from collections import OrderedDict
# flake8: noqa

# example was taken from the article 
# https://www.researchgate.net/publication/311825980_Identifying_Extract_Method_Refactoring_Opportunities_Based_on_Functional_Relevance
example = OrderedDict([
             (1, []),
             (2, ['manifests', 'rcs', 'length', 'rcs.length']), 
             (3, ['rcs', 'length', 'rcs.length', 'i']),
             (4, ['rec']),
             (5, ['rcs', 'i']),
             (6, ['rcs', 'i', 'rec', 'grabRes']),
             (7, ['rcs', 'i']),
             (8, ['rcs', 'i', 'rec', 'grabNonFileSetRes']),
             (9, []),
             (10, ['length', 'rec', 'j', 'rec.length']),
             (11, ['rec', 'j', 'name', 'rec.getName.replace', 'getName.replace', 'getName', 'replace']),
             (12, ['rcs', 'i']),
             (13, ['rcs', 'i', 'afs']),
             (14, ['rcs', 'i', 'afs', 'equals', 'afs.getFullpath', 'getFullpath', 'getProj;']),
             (15, ['name', 'afs', 'afs.getFullpath', 'getFullpath', 'getProj;', 'name.afs.getFullpath']),
             (16, ['rcs', 'i', 'afs', 'equals', 'afs.getFullpath', 'getFullpath', 'getProj;', 'afs.getPref;', 'getPref']),
             (17, ['afs', 'getProj;', 'afs.getPref;', 'getPref', 'pr']),
             (18, ['rcs', 'i', 'afs', 'equals', 'afs.getFullpath', 'getFullpath', 'afs.getPref;', 'getPref', 
                   'pr', 'pr.endsWith', 'endsWith']),
             (19,['pr']),
             (20,[]),
             (21,['name', 'pr']),
             (22,[]),
             (23,[]),
             (24,['name', 'name.equalsIgnoreCase', 'equalsIgnoreCase']),
             (25, ['manifests', 'rec', 'j', 'i']),
             (26,[]),
             (27,[]),
             (28,[]),
             (29, ['manifests', 'i']),
             (30, ['manifests', 'i']),
             (31,[]),
             (32,[]),
             (33, ['manifests']),
             (34,[]),
            ]
           )
