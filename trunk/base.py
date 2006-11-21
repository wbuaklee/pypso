#!/usr/bin/env python

import random
import math

class Particle:
  ''' data class for a particle entry '''
  def __init__(self,conf):
    self.bestSoFar = None
    self.next = list()
    self.velocity = list()
    self.current = list()
    self.best = list()
    for j in range(conf.dimensions):
      self.next.append(randMM(conf.initMin,conf.initMax))
      self.velocity.append(randMM(conf.initMin,conf.initMax))
      self.current.append(randMM(conf.initMin,conf.initMax))
      self.best.append(randMM(conf.initMin,conf.initMax))

  def __str__(self):
    ''' print the current position '''
    s = ''
    for d in self.current: s += str(d) + ', '
    return s

particles = None
pDelta = None
nDelta = None
gbest = None # may not be used, but it is needed in "star" topology and maybe logging
bestParticle = None    # same here
actRun = 1

def setup(conf,logging):
  ''' make a fresh start with a new population '''
  global particles, pDelta, nDelta, gbest, bestParticle, actRun

  # setup particle list
  particles = list()
  for i in range(conf.numberOfParticles):
    p = Particle(conf)
    particles.append(p)
  
  pDelta = list()
  nDelta = list()
  gbest = None
  bestParticle = None

  # set up particles' next location 
  for p in particles:
    for d in range(conf.dimensions):
      p.next[d] = randMM(conf.initMin,conf.initMax)
      p.velocity[d] = randMM(conf.deltaMin,conf.deltaMax)
    p.bestSoFar = None
    p.closeness = (abs(conf.initMin) + abs(conf.initMax)) / 2 
    p.geoneighbors = conf.k

  # setup pDelta and nDelta
  for d in range(conf.dimensions):
    pDelta.append(0)
    nDelta.append(0)
  
  # reset actrun and logs 
  if actRun == conf.averageOver + 1: 
    actRun = 1
    logging.logs = dict()    

# shortcuts for random operations
def rand(): return random.random()
def randMM(min,max): return random.uniform(min,max) 


def getAllNeighborsOf(p,conf):
  ''' Return neighbors of particle number p '''
  ns = list()
  nmbOfNbrs = 2 # circle
  if conf.topology == 'geographical':
    numbers = geofind(p,conf.k,conf)
    for n in numbers: ns.append(particles[n])
  else:
    if conf.topology == 'star': nmbOfNbrs = numberOfParticles - 1
    for i in range(nmbOfNbrs):
      ns.append(getNeighbor(p,i,conf))
  return ns

def getNumberOfNeighbors(conf):
  if conf.topology == 'circle': return 2
  elif conf.topology == 'star': return numberOfParticles -1
  elif conf.topology == 'geographical': return conf.k
  else: raise Exception(str(conf.topology) + ": No known topology specified!")
  
def getNeighbor(p,n,conf):
  ''' Return neighbor n of particle number p 
      for fixed topologies
  '''
  if conf.topology == 'circle':  # two neighbors each, 0 and 1
    if p==0 and n==0: return particles[conf.numberOfParticles-1]
    if p==conf.numberOfParticles-1 and n==1: return particles[0]
    elif n==0: return particles[p-1] 
    elif n==1: return particles[p+1]
    else: return list()
  if conf.topology == 'star':    # numberOfNeighbors-1 neighbors
    if n < p: return particles[n]
    elif n==conf.numberOfParticles: raise Exception('a particle can only have n-1 neighbors')
    elif n > p: return particles[n+1]
  else: return None 
    
  
def euclid(a,b,conf):
  ''' euclidean distance between particles a and b '''
  res = 0
  for d in range(conf.dimensions): res += pow((a.current[d]-b.current[d]),2)
  return math.sqrt(res)

def sumOver(n):
  ''' adds all numbers in range(n)  '''
  res = 0
  for i in range(n): res += i
  return res

def getNeighborWithBestFitness(pid,conf):
  ''' Return particle in p's neighborhood 
      with the best fitness 
  '''
  bestN = None
  l = []
  if conf.topology == 'star': bestN = bestParticle
  else:
    l = getAllNeighborsOf(pid,conf)
    bestN = l[0] # start with one of them
    bestSoFar = bestN.bestSoFar
    for n in l:
      if conf.isEqualOrBetterThan(n.bestSoFar,bestSoFar): 
        bestN = n
        bestSoFar = n.bestSoFar

  # a good spot to update some values
  for n in l:
    particles[pid].closeness += euclid(particles[pid],n,conf) # update closeness
  particles[pid].closeness /= float(len(l))
  # update geographic indices sum of neighbors
  particles[pid].geoneighbors_index_sum = 0
  if conf.logGeoRank:
    if conf.topology=='geographical':
      particles[pid].geoneighbors_index_sum = sumOver(conf.k - 1)
    if conf.topology=='star': 
      particles[pid].geoneighbors_index_sum = sumOver(conf.numberOfParticles - 1)
    else:
      gn = geofind(pid,conf.numberOfParticles-1,conf)
      for n in l:
        particles[pid].geoneighbors_index_sum += gn.index(particles.index(n))
  return bestN

def geofind(pid, nmb, conf):
  '''
    gets a list of  neighbors (well, their numbers) geographically:
    It widens the radius with a constant factor on each dimension
    until enough neighbors are in. It then sorts them according to
    the euclidean distance to the local particle.
  '''
  me = particles[pid]
  ns = set()
  rstep = me.closeness # the distance to the nearest neighbor in the last iteration 
  act_step = rstep
  # FOR THE MOMENT, THIS IS THE REALLY SIMPLE BRUTE FORCE APPROACH - THERE SHOULD BE SUBTLER WAYS, I KNOW - 
  # BUT AT LEAST I KNOW WHAT EXACTLY HAPPENS HERE
  #print act_step
  # while len(ns) < nmb:
  #   for p in range(len(particle)):  
  #     if not p==pid:
  #       isin = True
        #print 'for pid:' + str(pid) + ' - p is ' + str(p) + ',act_step is ' + str(act_step) + ' euclid is ' + str(euclid(particles[pid],particles[p],conf))
        #for d in range(dimensions):
          #print 'for pid:' + str(pid) + ' - p is ' + str(p) + ',act_step is ' + str(act_step) + ' ,dimension is ' + str(d) + ' and I\'ll compare ' + str(particles[p].current[d]) + ' with ' + str(me.current[d]) + ' and decide:' + str(not abs(particles[p].current[d]-me.current[d])>act_step)
          #if abs(particles[p].current[d]-me.current[d])>act_step: 
   #      if euclid(particles[pid],particles[p],conf)>act_step: 
   #        isin = False
          #break
   #      if isin: ns.add(p) 
      #if len(ns) >= nmb: break # !This actually means there could be still nearer ones we leave out.
                               # But: It makes the algorithm a lot faster. 
   #  if len(ns) < nmb: 
   #    act_step += rstep 
      #print 'not succesful-bigger radius'  
  # now we should have at least as many neighbors as we need, let's order them for euclidean distance
  l = []
  for i in range(len(particles)): 
    if not i==pid: l.append((euclid(particles[pid],particles[i],conf),i))
  l.sort()
  # and return as much as needed
  l2 = []
  for i in range(nmb): l2.append(l[i][1])
  return l2

def constrict(delta,conf):
  ''' Limit the change in a particle's 
      dimension value  
  '''
  if delta < conf.deltaMin:
    return conf.deltaMin
  else:
    if delta > conf.deltaMax:
      return conf.deltaMax
    else:
      return delta

def run(conf_file=''):
  ''' 
    run Particle Swarm Optimizer 
    @conf_file if a configuration-file name is specified, it is imported and used
     give the name of the file WITHOUT the .py - extension! see conf.py for more details
  '''
  if 'conf' in dir(): del conf  # eliminate configuration from earlier times
  # NOTE: Python seems not to care about this del - method. It's hard to reset values in a module
  #       just by reimporting it. If the conf-modules change, it's no problem though
  if not conf_file=='': exec("import %s as conf"%conf_file)
  else: import conf as conf
  if 'logging' in dir(): del logging # see comment above 
  import logging
  if 'fitness' in dir(): del fitness # see comment above
  import fitness

  moreTrials = True # there is always one - the default
  trials = conf.trialgen()
  while(moreTrials): # runs while there are more trial conditions
    global actRun
    logging.log[conf.actTrialName] = dict()
    logging.log[conf.actTrialName]['pBestLog'] = dict()
    logging.log[conf.actTrialName]['gBestLog'] = dict()
    logging.log[conf.actTrialName]['meanFitnessLog'] = dict()
    logging.log[conf.actTrialName]['georankLog'] = dict()
    logging.log[conf.actTrialName]['closenessLog'] = dict()
    logging.iterLog = {}
    logging.resetLogs(conf)

    if conf.logConsole:
      print '-----------------------------------------------------------------------------------------------'
      print 'Starting trial: ' + conf.actTrialName
      if not conf_file == '': print '  I used this config file: ' + str(conf_file)
      print '  dimensions: ' + str(conf.dimensions)
      print '  swarm size: ' + str(conf.numberOfParticles)
      print '  topology: ' + conf.topology
      print '  function: ' + conf.function
      print '  generations: ' + str(conf.maxIterations)
      if conf.averageOver > 1 : print '  averaged over ' + str(conf.averageOver) + ' runs'

    for r in range(conf.averageOver):
      iterations = 0 
      setup(conf,logging)
      if conf.logConsole: 
        print '----------------- run nr: ' + str(actRun).rjust(2) + ' in trial: ' + conf.actTrialName.ljust(20) + '------------------------------------'
        titlestr =  '                   '
        if conf.logMeanFitness: titlestr += 'mean fitness |'.rjust(15)
        if conf.logPBest: titlestr += 'mean pbest |'.rjust(15)
        if conf.logGBest: titlestr += 'gbest so far |'.rjust(15)
        if conf.logGeoRank: titlestr += 'avg. georank |'.rjust(15)
        if conf.logCloseness: titlestr += 'avg. closeness |'.rjust(10)
        print titlestr
        print '-----------------------------------------------------------------------------------------------'
      
      while iterations <= conf.maxIterations:
 
        sumFitness = 0
        sumPBests = 0
        # Make the "next locations" current and then 
        # test their fitness. 
        for p in particles:
          for d in range(conf.dimensions):
            p.current[d] = p.next[d]
          act_fitness = fitness.fitness(p,conf)
        
          # adjust personal best
          if conf.isEqualOrBetterThan(act_fitness,p.bestSoFar) or not p.bestSoFar:
            p.bestSoFar = act_fitness
            for d in range(conf.dimensions):
              p.best[d] = p.current[d]
        
          global gbest
          global bestParticle
          if bestParticle == None: bestParticle = particles[0]
          # reached new global best?
          if conf.isEqualOrBetterThan(act_fitness,gbest) or not gbest: 
            gbest = act_fitness
            bestParticle = p
        
          sumFitness += act_fitness
          sumPBests += p.bestSoFar
  
        # end of: for p in particles
  
          
        # recalculate next for each particle
        pid = 0
        for p in particles:
          n = getNeighborWithBestFitness(pid,conf)
          for d in range(conf.dimensions):
            # individual and soacial influence
            iFactor = conf.iWeight * randMM(conf.iMin,conf.iMax)
            sFactor = conf.sWeight * randMM(conf.sMin,conf.sMax)
            # this helps to compare against a form of random search
            if conf.random_search:
              pDelta[d] = randMM(conf.initMin,conf.initMax) - p.current[d]
              nDelta[d] = randMM(conf.initMin,conf.initMax) - p.current[d]
            else:
              pDelta[d] = p.best[d] - p.current[d] # the 'cognitive' orientation
              nDelta[d] = n.best[d] - p.current[d] # the 'social' orientation
            delta = (iFactor * pDelta[d]) + (sFactor * nDelta[d])
            
            # acceleration: gradually going from acc_max to acc_min ("cooling down")
            acc = conf.acc_max - ((conf.acc_max - conf.acc_min)/conf.maxIterations) * iterations 

            # calculating the next velocity from old velocity + individual and social influence
            new_vel = (p.velocity[d] * acc) + delta
            p.velocity[d] = constrict(new_vel,conf)
            # updating the next position 
            p.next[d] = p.current[d] + p.velocity[d]
          pid += 1
        # end of: for p in particles
       
        # log (if wanted) 
        if iterations in logging.iterLog:
          logging.logPoint(iterations, sumPBests / conf.numberOfParticles, gbest, sumFitness / conf.numberOfParticles,conf)
        
        if iterations in conf.logPopulationAt: logging.logPopulation(particles,iterations,actRun,conf)
        
        iterations += 1
      # end of: while iterations <= maxIterations 
      actRun += 1
      random.seed() # we should reseed the randomizer for each new run!  
    # end of one run, start new trial?

    try:
      conf.actTrialName = trials.next()
    except:
      moreTrials = False
  # end of trial - while

  logging.writeLog(conf)
# end of run() 



