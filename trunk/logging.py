import conf
import base

def getLogPoints(runs,interval):
  res = []
  while(runs>=0):
    res.append(runs)
    runs -= interval
  return res
  
log = dict() # contains logs for all trials (trialname is the key)
iterLog = getLogPoints(conf.maxIterations,conf.logFrequency) # just lists the logpoints

def logPoint(when,pBestAvg,gBest,meanFitness):
  ''' logging - just adding up values for iteration points
      writeLog() will average them
  '''	  
  # compute avg nearness
  avg_nearness = 0
  avg_geo_index = 0
  for p in base.particles: 
    avg_nearness += p.nearness
    p.geoneighbors_index_sum /= base.getNumberOfNeighbors()
    avg_geo_index += p.geoneighbors_index_sum
  avg_nearness /= float(conf.numberOfParticles)
  avg_geo_index /= float(conf.numberOfParticles) 
  if conf.logConsole: print 'iteration: ' + str(when).rjust(4) + '\t' + str(meanFitness)[:10].rjust(15) + '\t' + str(pBestAvg)[:10].rjust(15) + '\t' + str(gBest)[:10].rjust(15) + '\t' + str(avg_geo_index).rjust(15) + '\t' + str(avg_nearness).rjust(10) 
  if conf.logMeanFitness: log[conf.actTrialName]['meanFitnessLog'][str(when)] += meanFitness
  if conf.logPBest: log[conf.actTrialName]['pBestLog'][str(when)] += pBestAvg
  if conf.logGBest: log[conf.actTrialName]['gBestLog'][str(when)] += gBest
  if conf.logGeoRank: log[conf.actTrialName]['georankLog'][str(when)] += avg_geo_index
  if conf.logNearness: log[conf.actTrialName]['nearnessLog'][str(when)] += avg_nearness
  
def resetLogs():
  for p in iterLog: # this is useful for averaging
    log[conf.actTrialName]['meanFitnessLog'][str(p)] = 0
    log[conf.actTrialName]['pBestLog'][str(p)] = 0
    log[conf.actTrialName]['gBestLog'][str(p)] = 0
    log[conf.actTrialName]['georankLog'][str(p)] = 0
    log[conf.actTrialName]['nearnessLog'][str(p)] = 0

def getNumberOfLogs(include):
  ''' returns number of logged Fitness values (1-3) 
      include can be 'geo', 'fitness' or 'all'
  '''
  res = 0
  if include in ('all','fitness') and conf.logMeanFitness: res += 1
  if include in ('all','fitness') and conf.logPBest: res += 1
  if include in ('all','fitness') and conf.logGBest: res += 1
  if include in ('all','geo') and conf.logGeoRank: res += 1
  if include in ('all','geo') and conf.logNearness: res += 1
  return res

def writeHeaders(include):
  ''' write Headers 
      include can be 'geo', 'fitness' or 'all'
  '''
  headers = [] # headers of the log file
  for trial in log.keys():
    if include in ('all','fitness') and conf.logMeanFitness: headers.append('mean fitness ('+trial+')')
    if include in ('all','fitness') and conf.logPBest: headers.append('avg. pbest ('+trial+')')
    if include in ('all','fitness') and conf.logGBest: headers.append('gbest so far ('+trial+')')
    if include in ('all','geo') and conf.logGeoRank: headers.append('avg. georank ('+trial+')')
    if include in ('all','geo') and conf.logNearness: headers.append('avg. nearness ('+trial+')')
  return headers


def getColumnSequence(start,data_type):
  s = []
  for trial in range(len(log.keys())):
    if data_type=='fitness':
      for i in range(getNumberOfLogs('fitness')): s.append(start+i)
      start += getNumberOfLogs('all')
    elif data_type=='geo':
      for i in range(getNumberOfLogs('geo')): s.append(start+i)
      start += getNumberOfLogs('all')
  return s

def writeGNURFile(data_type): 
  ''' write a GNU R File
      data_type can be 'fitness' ot 'geo' (those are groups of data that 
      would fit well on the same scale, per topic and per scale) 
  '''
  headers = writeHeaders(data_type)
  rFile = open('log'+conf.logSuffix+'_'+data_type+'.r','w')
  import datetime
  rFile.write('# ---------------------------------------------------------------------------\n')
  rFile.write('# This file was automagically outputted by the PyPSO script on ' + datetime.date.today().strftime("%m-%d-%y" + '\n'))
  rFile.write('# Call "R --no-save < log'+conf.logSuffix+'_'+data_type+'.r" to let it run and create JPG graphs\n')
  rFile.write('# ---------------------------------------------------------------------------\n')
  rFile.write('jpeg("log'+conf.logSuffix+'_'+data_type+'.jpg")\n')
  rFile.write('d <- read.table("log'+conf.logSuffix+'.csv", sep=",", header=TRUE)\n')
  # first draw the plot space, lines will come later. It's important which column gets to define the Y axis!
  # I think it's best to take the one with the most critical value, so the granularity will be the highest for its values...
  # If geographical data is measured, values are alway good if they're low.
  # So here comes the heuristic:
  # find out what is measured, then find best scale for that (assumes an ordering in output of the columns!) 
  if data_type=='geo' or conf.isEqualOrBetterThan(1,2): func = min
  else: func = max
  tmp = None
  bestCol = None
  t = 0
  for trial in log.keys():
    for col in log[trial].keys(): # find critical column
      if (col=='meanFitnessLog' and (data_type=='geo' or not conf.logMeanFitness)): continue
      if (col=='pBestLog' and (data_type=='geo' or not conf.logPBest)): continue
      if (col=='gBestLog' and (data_type=='geo' or not conf.logGBest)): continue
      if (col=='georankLog' and (data_type=='fitness' or not conf.logGeoRank)): continue
      if (col=='nearnessLog' and (data_type=='fitness' or not conf.logNearness)): continue
      for row in log[trial][col].values():
        if not tmp: tmp = row
        if func(row,tmp) == row: 
          bestCol = (t,col)
          tmp = row
    t += 1

  # for fitness data, get the actual column in the outputted data 
  if bestCol[1]=='meanFitnessLog' or (bestCol[1]=='pBestLog' and not conf.logMeanFitness) or (bestCol[1]=='gBestLog' and not conf.logMeanFitness and not conf.logPBest) : index = 1 
  elif bestCol[1]=='gBestLog' and conf.logGBest and conf.logMeanFitness and conf.logPBest: index = 3
  elif (bestCol[1]=='pBestLog' and conf.logMeanFitness) or (bestCol[1]=='gBestLog' and (not conf.logMeanFitness or not conf.logPBest)): index = 2
  
  # for geodata, it's simpler:
  nfl = getNumberOfLogs('fitness')
  if bestCol[1]=='georankLog': index = nfl + 1
  elif bestCol[1]=='nearnessLog': index = nfl + 2
  
  #index *= bestCol[0] # shift it to the trial with the best value
  for i in range(bestCol[0]): index += getNumberOfLogs('all')
  index += 1 # the first column are the iterations, so add one
  # Here I assume that it's cool to show the y-column for fitness data logarythmic! You might want to change that!
  if data_type=='fitness': logarythmic = 'y'
  else: logarythmic = ""
  rFile.write('plot(d$Iteration,d[,'+str(index)+'],type="n",log="'+logarythmic+'", xlab="Iteration", ylab="Fitness")\n')

  # generate colors
  colors = ['black','green','yellow','red','blue','pink','orange','grey']
  trial_colors = []
  for trial in log.keys():
    for i in range(getNumberOfLogs(data_type)):
      trial_colors.append(colors[log.keys().index(trial)])

  # write the lines ...
  def plotLine(column,nmb,color): rFile.write('lines(d$Iteration,d[,'+str(column)+'], lty='+str(nmb)+', col="'+ color +'")\n')

  start = 2 # the data in R starts indexing by 1 since we have the Iteration column, which is the index, not data
  if data_type == 'geo': start += nfl
  used_colors = []
  columns = getColumnSequence(start,data_type)
  nmb = start
  for trial in headers:
    color = trial_colors[nmb-start]
    used_colors.append(color)
    plotLine(columns[nmb-start],nmb-start+1,color)
    nmb += 1
	#column += 1
	# step over columns in the data that we are not considering here
	#if data_type=='fitness' and: column += getNumberOfLogs('geo')
	#if data_type=='geo': column += getNumberOfLogs('fitness')

  # ... and the legend (its horizontal position is just an estimate)
  rFile.write('legend('+str(conf.maxIterations/3)+',max(d[,'+str(index)+'])-max(d[,'+str(index)+'])/10,lty=c'+str(tuple(range(1,nmb-start+1))).replace(",)",")")+',legend=c'+str(tuple(headers)).replace(",)",")")+', col=c'+str(tuple(used_colors)).replace(",)",")")+')\n')

  rFile.write('dev.off()\n')
  rFile.write('q()\n')
  rFile.close()

def writeLog():
  # filetype
  suffix = '.csv'
  logFile = open('log'+conf.logSuffix+suffix,'w')
  if not(logFile==None):
    # average out
    for trial in log.keys():
      if conf.logPBest: 
        for when in iterLog: log[trial]['pBestLog'][str(when)] = float(log[trial]['pBestLog'][str(when)]) / conf.averageOver
      if conf.logGBest: 
        for when in iterLog: log[trial]['gBestLog'][str(when)] = float(log[trial]['gBestLog'][str(when)]) / conf.averageOver
      if conf.logMeanFitness: 
        for when in iterLog: log[trial]['meanFitnessLog'][str(when)] = float(log[trial]['meanFitnessLog'][str(when)]) / conf.averageOver
      if conf.logGeoRank: 
        for when in iterLog: log[trial]['georankLog'][str(when)] = float(log[trial]['georankLog'][str(when)]) / conf.averageOver
      if conf.logNearness: 
        for when in iterLog: log[trial]['nearnessLog'][str(when)] = float(log[trial]['nearnessLog'][str(when)]) / conf.averageOver
    
    # rather explicit, but another logging style could be implemented with this helpers
    def writeCell(val, isLast): 
        colon = ','
        if isLast: colon = ''
        return str(val) + colon
    def writeNewLineStart(): return ''
    def writeNewLineEnd(): return '\n'
    
    l = len(log.keys()) # number of trials
    numCols = 0

    headers = writeHeaders('all')
	  
    logFile.write(writeCell('Iteration',False))
    for h in headers:
      logFile.write(h)
      if headers.index(h)<len(headers)-1: logFile.write(',')
    logFile.write('\n')

    # write data
    iterLog.sort()
    for iteration in iterLog: 
	  # write a string and then 
      logFile.write(writeNewLineStart() + writeCell(iteration,False))     
      for i in range(l):
        trial = log.keys()[i]
        if conf.logMeanFitness: logFile.write(writeCell(log[trial]['meanFitnessLog'][str(iteration)], i==l-1 and not (conf.logPBest or conf.logGBest or conf.logGeoRank or conf.logNearness)))
        if conf.logPBest: logFile.write(writeCell(log[trial]['pBestLog'][str(iteration)], i==l-1 and not (conf.logGBest or conf.logGeoRank or conf.logNearness)))
        if conf.logGBest: logFile.write(writeCell(log[trial]['gBestLog'][str(iteration)], i==l-1 and not (conf.logGeoRank or conf.logNearness)))
        if conf.logGeoRank: logFile.write(writeCell(log[trial]['georankLog'][str(iteration)], i==l-1 and not conf.logNearness))
        if conf.logNearness: logFile.write(writeCell(log[trial]['nearnessLog'][str(iteration)], i==l-1))
      logFile.write(writeNewLineEnd())

  logFile.close()

  # write GNU R File(s), if requested
  if conf.logRFile:
    if conf.logMeanFitness or conf.logPBest or conf.logGBest: writeGNURFile('fitness')
    if conf.logGeoRank or conf.logNearness: writeGNURFile('geo')


