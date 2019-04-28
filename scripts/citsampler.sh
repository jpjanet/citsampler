#!/usr/bin/env python3

# direct console script to call python module from shell
# JP Janet


from citsampler.sampler import sampler
import sys

def main():
    """
    Console access point to src.sampler, used to generate samples from a
    constrained hypercubde defined by the input file. Reads from system
    arguments and should be called with <inputfile> <outputfile> <samples>
    """
    args = sys.argv[1:]
    if not len(args) == 3:
        print('Wrong number of arguments. Please invoke this script with <inputfile> <outputfile> <samples>')
        
    else:
        args = {'inputFile':sys.argv[1],'outputFile':sys.argv[2],
                'nResults':int(sys.argv[3])}
        
        # invoke function 
        sys.exit(sampler(**args))
    
if __name__ == '__main__':
    main()
