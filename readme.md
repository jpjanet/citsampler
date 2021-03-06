[![Build Status](https://travis-ci.org/jpjanet/citsampler.svg?branch=master)](https://travis-ci.org/jpjanet/citsampler)

Citsampler
==========
Written by JP Janet

Introduction
------------
This repo contains a simple, single-function python module for the generation of valid sample points from an n-dimensional unit hypercube subject to a set of nonlinear contraints, given the constraints and an example interior point. The user provides a custom number of valid points to return and the goal is to maximize the dissimilarity of the valid points returned. The basic apporach used is a two-step process:

### Phase 1: Rejection sampling MCMC
The first phase attempts to find a large number of valid points (default 5x the requested number) using rejection-sampling Markov Chain Monte Carlo (MCMC). Starting from the initial value, proposed steps are taken by drawing a random vector on the hypercube and then proposing a new point on the ray connecting the random vector and current state. The new point is only accepted if it is valid (as per the constraints), otherwise a new point is drawn. The step length is dynamically varied during operation to keep the acceptance ratio over the last 100 steps in a fixed range (0.2-0.25,a heuristic for good mixing). If too many points are being rejected, the step size is reduced such that the proposed points are more similar to the existing points, and vice-versa. Some sensitivity to these parameters were observed in testing and good performance might require tuning them for a given application. Multiple chains (default 6) will be run for a single target, and all of the valid points are aggregated and passed to phase 2. The maximum number of iterations per chain are configured based on the number of selected points. 

### Phase 2: k-medoids clustering
The collection of valid points from MCMC are then handed to a k-medoids clustering routine (portioning around medoids, or [PAM](https://en.wikipedia.org/wiki/K-medoids)). This extracts a well-separated set of points of the target number to print. K-medoids is similar to k-means except all centroids are restricted to elements of the set, and so we are guaranteed all points produced are valid. This dependents on the pyclustering toolbox which in turns calls some highly-optimized c++ code and can perform this clustering rapidly even for 1000s of centroids out of 10s of the thousands of points, though the this will of course become the limiting factor as the number of points and dimension increases.

Simple extensions to this code can result would be a) use of Sobol points for sampling, generally known to give better convergence in high-dimensional integration (making a quasi-Monte Carlo method) and b) stagewise restarting of the MCMC process on centroid points to generate better coverage. Also it should be pointed out that this script currently discards about 90% of the generated feasible points and some applications may want to retain the full set. The approach was motivated by the general efficiency of MCMC as a method for high-dimensional integration and the method is expected to extend to higher dimensions than the training examples (max 11), possibly with longer max chain steps. One clear drawback of this approach is that it handles the constraints in a totally black-box manner, meaning it cannot exploit any structure in the problem.

From a code perspective, this is implemented as a python module due to the great ecosystem for multiplatform  deployment and my previous experience. [Sphinx](http://www.sphinx-doc.org/en/master/) is used to generate documentation and a testing pipeline using [pytest](https://docs.pytest.org/en/latest/) and [Travis CI](https://travis-ci.org/) is used to test both python functions and the connection to the shell. 


Requirements
------------
This software is written and test in Python 3.6. It has the following dependencies:

1) Python (3.6.5)
2) [numpy](https://www.numpy.org/) (1.16.3)
3) [pyclustering](https://github.com/annoviko/pyclustering) (0.9.0)
4) [setuptools](https://pypi.org/project/setuptools/) (39.0.1)

Setuptools is required for manual installation only. The versions indicated are those tested, compatibly with other versions is likely but not assured. Note that pyclustering itself requires [Pillow](https://pillow.readthedocs.io/en/stable/), [matplotlib](https://matplotlib.org/) and [scipy](https://www.scipy.org/).


Installation 
------------
The recommended method of installation is to use a package manager such as [pip](https://pypi.org/project/pip/). From the base directory, call

`$ pip install ./`

This will handle requirements automatically. This is all you need to do, if you are using pip.

Alternatively, a direct python install can be done once the requirements are met. This can be easily done with

`$ pip install -r requirements.txt`

or by any other means. To install Citsampler, run

`$ python setup.py install`



Example of use
--------------
The basic usage of citsampler is through the provided console hook and is as follows:

`$ citsampler <inputfile> <outputfile> <number_of_points>`

Sample input file examples are provided under `examples/`. A functional call could be:

`$ citsampler examples/alloy.txt alloy-output.txt 1000`
  
For compatibility  with the prompt, this is also packaged into a bash script, `scripts/citsampler.sh`, which should be made executable (`chmod u+x scripts/citsampler.sh` in Bash) and then run with:
 
`$ scripts/citsampler.sh <inputfile> <outputfile> <number_of_points>`
 

Documentation
-------------
Basic API documentation is online [here](https://citsampler.readthedocs.io/en/latest/).


