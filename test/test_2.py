import subprocess
from citsampler.sampler import sampler
from citsampler.constraints import Constraint 
from pkg_resources import resource_filename, Requirement

def test_1(tmpdir):
    """ regression test for mixture.txt case
        using console
    """
    # set paramteters
    infile =resource_filename(Requirement.parse("citsampler"),'/examples/mixture.txt')
    outfle = tmpdir + '/mixture.out'
    
    # run the code using console!
    p = subprocess.call(['citsampler',infile,outfle,'450']) 
    
    
    
    # check the points are valid
    points = []
    with open(outfle,'r') as f:
        for line in f.readlines():
            points.append(list([float(i) for i in line.strip().split(' ')]))
            
    constraint = Constraint(infile)        
    outcomes = list([constraint.apply(x) for x in points])
    
    # assert check
    assert len(points) == 450
    assert any(outcomes)
