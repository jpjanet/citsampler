from citsampler.sampler import sampler
from citsampler.constraints import Constraint 
from pkg_resources import resource_filename, Requirement

def test_1(tmpdir):
    """ regression test for alloy.txt case
    """
    # set paramteters
    infile = resource_filename(Requirement.parse("citsampler"),'/examples/alloy.txt')
    outfle = tmpdir + '/alloy.out'
    
    # run the code
    sampler(infile,outfle,1000)
    
    # check the points are valid
    points = []
    with open(outfle,'r') as f:
        for line in f.readlines():
            points.append(list([float(i) for i in line.strip().split(' ')]))
            
    constraint = Constraint(infile)        
    outcomes = list([constraint.apply(x) for x in points])
    
    # assert check
    assert len(points) == 1000
    assert any(outcomes)
