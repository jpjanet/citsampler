Citsampler
==========
Written by JP Janet

Introduction
------------
This repo contains a simple, single-function python module for the generation of valid sample points from n-dimensional unit hypercube subject to a set of nonlinear contraints, given the constraints and an example interior point. The user provides a custom number of valid points to return and the goal is to maximize the dissimilarity of the valid points retuned. The basic apporach used  is a two-step process:

### Phase 1: Rejection sampling MCMC
The first phase attemps to find a large number of valid points (default. 5x the requested number) using rejection-sampling markov chain monte carlo (MCMC). Starting from the initial value, proposed steps are taken by drawing




Requirements
------------
This software is written and test in Python 3.6. It has the following dependenices:

1) python 3.6
2) numpy
3) pyclustering

Note that pyclustering itself requires Pillow,


Intsallation 
------------


Example of use
--------------


Documentation
------------


