Citsampler
==========
Written by JP Janet

Introduction
------------
This repo contains a simple, single-function python module for the generation of valid sample points from n-dimensional unit hypercube subject to a set of nonlinear contraints, given the constraints and an example interior point. The user provides a custom number of valid points to return and the goal is to maximize the dissimilarity of the valid points retuned. The basic apporach used  is a two-step process:

### Phase 1: Rejection sampling MCMC
The first phase attemps to find a large number of valid points (default. 5x the requested number) using rejection-sampling markov chain monte carlo (MCMC). Starting from the initial value, proposed steps are taken by drawing




<a name="Requirements">Requirements</a>
------------
This software is written and test in Python 3.6. It has the following dependenices:

1) Python (3.6.5)
2) [numpy](https://www.numpy.org/) (1.16.3)
3) [pyclustering](https://github.com/annoviko/pyclustering) (0.9.0)
4) [setuptools](https://pypi.org/project/setuptools/) (39.0.1)

Setupy tools is required for mannual installation only. The versions indicated are those tested, compatibliy with other versions is likely but not assured. Note that pyclustering itself requires [Pillow](https://pillow.readthedocs.io/en/stable/), [matplotlib](https://matplotlib.org/) and [scipy](https://www.scipy.org/).


Intsallation 
------------
The reccomended method of installation is to use a package manager such as [pip](). From the base directoty, call

`pip install ./`

This will handle requirements automatically. Alternatively, a direct python install can be done once the [requirements](Requirements) are met. This can be easily done with

`pip install -r requirements.txt`

or by any other means. To install Citsampler, run

`python setup.py install`



Example of use
--------------
The basic usage of citsampler is through the provided console hook and is as follows:

`$ citsampler <inputfile> <outputfile> <number_of_points>`

Provided input file examples are provided under `examples/`. An functional call could be:

`$ citsampler examples/alloy.text alloy-output.txt 1000`
  
 For compatibliy with the prompt, this is also packaged into a bash script, `scripts/citsampler.sh`, which should be made executable (`chmod u+x scripts/citsampler.sh` in Bash) and then run with:
 
`$  scripts/citsampler.sh <inputfile> <outputfile> <number_of_points>`
 

Documentation
------------


