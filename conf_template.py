# a template for an experiment - see conf.py for details

actTrialName = 'circle' 
numberOfParticles = 75
maxIterations = 300
acc_max = 1.0
acc_min = 0.4
topology = 'circle' 
k = 2

deltaMin = -4
deltaMax =  4

iWeight = 1.5
iMin = 0.0   
iMax = 1.0   
sWeight = 1.5
sMin = 0.0  
sMax = 1.0  

random_search = False 
def isEqualOrBetterThan(a,b): return a <= b
initMin = -15
initMax = 15
dimensions = 10 
function = 'sphere'

logPBest = True
logGBest = True
logMeanFitness = False
logGeoRank = True    
logCloseness = True
 
logSuffix = '_cg_sphere' 
logRFile = True   
logConsole = True
logFrequency = 1

averageOver = 30  
def trialgen():
  global topology
  topology = 'geographical'
  yield 'geographical'
