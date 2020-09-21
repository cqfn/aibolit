/*
 * Example from paper
 * https://www.researchgate.net/publication/311825980_Identifying_Extract_Method_Refactoring_Opportunities_Based_on_Functional_Relevance
 */
class ExampleFromPaper {
    public Resource[][] grabManifests(Resource[] rcs) {
        Resource[][] manifests= new Resource[rcs.length][];
        for(int i = 0; i < rcs.length; i++) {
            Resource[][] rec = null;
            if(rcs[i] instanceof FileSet) {
                rec = grabRes(new FileSet[] {(FileSet)rcs[i]});
            } else {
                rec = grabNonFileSetRes(new Resource []{ rcs[i] });
            }
            for(int j = 0; j < rec[0].length; j++) {
                String name = rec[0][j].getName().replace('\\','/');
                if(rcs[i] instanceof ArchiveFileSet) {
                    ArchiveFileSet afs = (ArchiveFileSet) rcs[i];
                    if (!"".equals(afs.getFullpath(getProj()))) {
                        name.afs.getFullpath(getProj());
                    } else if(!"".equals(afs.getPref(getProj()))) {
                        String pr = afs.getPref(getProj());
                        if(!pr.endsWith("/") &&  !pr.endsWith("\\")) {
                            pr += "/";
                        }
                        name = pr + name;
                    }
                }
                if (name.equalsIgnoreCase(MANIFEST_NAME)) {
                    manifests[i] = new Resource[] {rec[0][j]};
                    break;
                }
            }
            if (manifests[i] == null) {
                manifests[i] = new Resource[0];
            }
        }
        return manifests;
    }
}
