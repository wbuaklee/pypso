#!/usr/bin/env python

actTrialName = 'circle' # Name of the trial with original settings, e.g. "d=10", can also be ""
                        # see trialgen() how to create more trials with changed conditions
numberOfParticles = 125
maxIterations = 500
# acceleration factor ("cooling down" the system over time)?
acc_max = 0.98
acc_min = 0.4

topology = 'circle' # one out of circle|geographical|star
# NOTE: "circle" means 2 neighbors each, "star" means global connection
#       "geographical" always selects the k nearest neighbors
k = 2
# TODO: topology wheel?

# set limits for location changes, so particles far from the best don't build up too much speed 
deltaMin = -4
deltaMax =  4

# set individuality and sociality 
iWeight = 1.5
iMin = 0.0  # low  stochastic weight factor 
iMax = 1.0  # high stochastic weight factor 
sWeight = 1.5
sMin = 0.0  # low  stochastic weight factor 
sMax = 1.0  #  high stochastic weight factor 

random_search = False # Switch this on to compare your performance against random search.
                      # This will not use social or cognitive measures, but a random value for orientation. 
# ********************************************
# The next variables are related to the problem solution space. 
# See function "test" for definition of fitness function. 
# ********************************************
# To avoid hardwiring <(=) or >(=) in the code, say here how you like your fitness (low or high)
# Return True if a is equal or "better" than b (in terms of their desired fitness values)
def isEqualOrBetterThan(a,b): return a <= b
# initialization boundaries, a range in which you put all particles' dimensions
initMin = -15
initMax = 15
dimensions = 10 # dimensionality of solution space 
function = 'griewank' # one out of sphere|rosenbrock|rastrigin|griewank - see fitness() for implementation 

# ******************************************
# These variables control logging of the results
# ******************************************
# NOTE: "logging" means saving some values along the way in a file, so it can be plotted as graph.
#       You can also turn logging (of all information) on the console on or off
logPBest = True        # log average personal bests
logGBest = True        # log the global best
logMeanFitness = False # log the mean fitness
# the next two options are computationally expensive (if you're not having geographical topology set anyway)
logGeoRank = True      # log the average rank of neighbors of particles in terms of geographical distance
logNearness = True    # log the average of the distances particles have to their neighbors
 
# Logging style: "csv"-files, meaning comma separated value files 
# (usable in MS Excel, Open Office or the like - see below for GNU R!)
logSuffix = '_gc_griewank' # suffix for the logfile name("log{logSuffix}.[csv|html]")
logRFile = True   # for the.csv - data, you can generate a GNU R - File. It will plot your CSV data immediately
                  # (just type "R --no-save < log{logSuffix}.r" when GNU R is installed) 
                  # You don't even need to know GNU R! (though it is a nice, highly customable tool)
logConsole = True # any activity output on console?
logFrequency = 10 # log point every n iterations (should be a divisor of maxIterations!)

# ******************************************
# These variables control experiment setup
# ******************************************
averageOver = 30  # make this many runs and average over them at each log point - usually this is set to "1"
def trialgen():
  ''' this helps to compare several trials with changed conditions
      change a condition and yield a name for the trial, for example:
        global dimensions
        dimensions = 20
        yield "d=20" 
      Do this for each condition that you want to compare the original setup conditions with.
      Just type "pass" if you don't want to compare conditions. 
  '''
  global topology
  #topology = 'star'
  #yield 'star' 
  topology = 'geographical'
  yield 'geographical'
  #global random_search
  #random_search = True
  #yield 'random search'
  #pass
