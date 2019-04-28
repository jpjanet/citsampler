# Simple rejection-sampling MCMC approach to generate 
# dissimlar points from constrained hypercube
# JP Janet


# imports
import os, sys, time
import numpy as np 
from src.constraints import Constraint # load the constraint class hanlder
from pyclustering.cluster.kmedoids  import kmedoids # load the clustering alg

def outputWriter(filepath, data):
    """
    Defines a monte carlo sampler for constrained
    high-dimenisonal integration using rejection sampling
    
    :param filepath: string, path to output file
    :param data: np array, data to write
    """
    
    with open (filepath,'w') as f:
        for row in data:
            f.write(" ".join([str(i) for i in row])+'\n')

class constrainedMCMC:
    """
    Defines a monte carlo sampler for constrained
    high-dimenisonal integration using rejection sampling
    
    :param constraint: constraint class object defining the task
    :param stepsize: float in [0,1], starting stepsize
    """
    
    def __init__(self,constraint,stepsize):
        """
        Constructor, binds args to the 
        high-dimenisonal integration using rejection sampling
  
        """
        # bind attirbutes
        self.constraint =  constraint
        self.state = np.array(self.constraint.get_example())
        self.dim = self.constraint.get_ndim()
        self.stateHistory = [self.state]
        self.stepsize = stepsize
        
        # intialize trajectory
        self.steps = 0
        self.ar = 1 # total acceptance ratio 
        self.ar100 = 1 # accptance ratio, last 100 samples
        
    def proposalDistribution(self):
        """
        Proposal distribution for MCMC, generates new sample
        based on the current state and stepsize by combination
        with a random vector on the self.dim hypercube
        """
        
        return (1.0-self.stepsize)*self.state + self.stepsize*(np.random.rand(self.dim))        
    
    def step(self):
        """
        Take one step of rejection-sampling MCMC and update
        the resutling acceptance ratios
        """
        
        # generate proposal
        proposal = self.proposalDistribution()    
        # rejection sampleing
        if self.constraint.apply(proposal): # accept
            # note, we save only valid states in history
            self.stateHistory.append(self.state)
            # move to new state
            self.state = proposal
             # update accept rates
            self.ar =  (self.ar*self.steps +1)/(self.steps+1)
            self.ar100 = (self.ar100*99 +1)/(100)
        else:  # reject
            # update accept rates, state does not move
            self.ar =  (self.ar*self.steps)/(self.steps+1)
            self.ar100 = (self.ar100*99)/(100)
        # update counter
        self.steps += 1
    
def rsMcmcPhase(constraint, targetSamples, numChains = 5,               
                maxIts = False, minIts = False,
                targetArLow = 0.05, targetArHigh = 0.25,
                stepModifier = 1.05):
    """
    Perform multi-chain rejection-sampling MCMC on the provided constraint object

    :param constraint: constraint class object defining the task
    :param targetSamples: int, number of valid points to seek per chain
    :param maxIts: int, maximum iterations per chain
    :param minIts: int, minimum iterations per chain    
    :param targetArHigh: float in [0,1], maximum 100-step ar before step is increased
    :param targetArLow: float in [0,1], minimum 100-step ar before step is reduced 
    :param stepModifier: float >1, ammount to modify stepsize by
    :return: np.ndarray, valid points from all chains (my contain duplicates)
    """

    # set iteration control if not provided
    if not maxIts:
        # max number of chain iterations to perform
        # 500k or 100 per sample, at least
        maxIts = max(5e5,1e2*targetSamples) 
    
    if not minIts:
        # minimum number of chain iterations to perform
        # between 5 x target samples or 5000
        # cannot be more than maxIts, 
        minIts = min(max(5*targetSamples,5000),maxIts)
    
    # repeat numChains times:
    for cn in range(0,numChains):
        
        # time per chain
        chainTime = time.time()

        # create the MCMC chain 
        mc = constrainedMCMC(constraint,1.0)
        
        # loop control
        terminate = False 
        while not terminate:
            # advance mcmc
            mc.step()
            
            # mixing control by checking acceptance rate over last 100 steps
            if not mc.steps %100 and mc.steps > 0:
                if mc.ar100 < targetArLow:
                    # if local ar is too low, make step smaller
                    mc.stepsize = max(mc.stepsize/stepModifier,1e-18)
                elif mc.ar100 > targetArHigh:
                    # if local ar is too high, make step bigger
                    mc.stepsize = min(stepModifier*mc.stepsize,1)
                    
            # check for max interations reached
            if mc.steps >= maxIts:
                print('Could not find enough samples in '+ str(maxIts) + ' iterations.')
                terminate = True
            # check if targerSamples and min interation criteria are reacehd
            elif len(mc.stateHistory) >= targetSamples and mc.steps >= minIts:
                terminate = True


        # save sampled points:
        if not cn: 
            mcdata = np.array(mc.stateHistory)
        else:
            mcdata = np.row_stack([mcdata,np.array(mc.stateHistory)])
            
        # print status of chain
        msg = 'mc chain ' +  str(cn) + ': found '+ str(len(mc.stateHistory)) + ' valid points in '\
            + str(mc.steps)+ ' iterations taking ' \
            +  str(round(time.time() - chainTime,2)) + ' seconds'
        print(msg)
    
    return(mcdata)       

def sampler(inputFile,outputFile,nResults):
    """
    Function to find nResults spanning points satisfying the constraints given 
    in the inputFile, and write them to outputFile

    :param inputFile: string, path to input file
    :param outputFile: string, target output file
    :param nResults: int, number of results to find
    :return: int, outcome flag (0=normal, 1=error)
    """
    
    # start total timer
    startTime = time.time()
    
    # test the file exists
    try:
        constraintInstance =  Constraint(fname=inputFile)
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        sys.exit(1)
    except:
        print('Uncaught error in importing constraint file')
        sys.exit(1)
    
    
    # params for MCMC run, could be read in as input instead
    # number of chains to run
    numChains = 6  
    # number of results to seek per chain
    targetSamples=5*nResults

    # start mcmc clock
    mcStart = time.time()

    # do mcmc operation
    mcdata = rsMcmcPhase(constraint=constraintInstance,targetSamples=targetSamples,numChains=numChains)

    # trim out any duplicates
    mcdata = np.unique(mcdata, axis=0)

    # end clock and print mcmc status
    msg = 'MC phase complete, found a total of ' + str(mcdata.shape[0]) + \
          ' unique interior points in '+ str(round(time.time() - mcStart,0)) + ' seconds'
    print(msg)
    
    # determine if the correct number of points have been found
    if mcdata.shape[0] <= nResults:
        print('could not find target number of points, writing what is available')
        outputWriter(filepath = outputFile, data = mcdata)
        exitStatus = 1 # error 
    else:
        clusterStart = time.time()
        print('starting clustering phase, seeking ' + str(nResults) + ' medoids')

        # random initial medoids
        startMeds = np.random.randint(low=0,high=mcdata.shape[0],size=nResults)

        # create cluster instance
        kmed  = kmedoids(data=mcdata,initial_index_medoids=startMeds,tolerance=1e-10)

        # run cluster
        kmed.process()

        # return centers
        medoids = mcdata[kmed.get_medoids(),:]

        msg = 'cluster phase complete, found a total of ' + str(medoids.shape[0])  \
            + ' interior points from '+  str(mcdata.shape[0])  \
            + ' in ' + str(round(time.time()-clusterStart,0)) + ' seconds'
        print(msg)    
        
        # test if the correct number of results are returned 
        if medoids.shape[0] == nResults:
            exitStatus = 0
        else:
            msg = 'incorrect number of resutls obtained from clustering, writing '  \
                +  str(medoids.shape[0]) + ' points to '+ outputFile
            print(msg)
            exitStatus = 1
    
        # write results
        outputWriter(filepath = outputFile, data = medoids)
        
        # print final time
        msg = 'routine complete in ' + str(round(time.time() - startTime,0)) + ' seconds'
        print(msg)   
        
        return(exitStatus)    
        
   
    