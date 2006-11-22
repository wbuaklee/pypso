##################################################################
# This script is not incorporated into pypso.
# It was a helper for me to generate plots of variance in the saved
# populations dimensionwise.
# It can be used, but some things are non-dynamic (I had no time to
# do it for all purposes yet).
# This could be used for an option "logVariance" or so...
##################################################################
topologies = ['circle','geographical']
runs = 30
logPoints = [100,200,300,400,500]
functions = ['griewank'] #['sphere','rastrigin','griewank']
dimensions = 10

f = open('var.r','w')
for func in functions:
  f.write('jpeg("variation_'+func+'.jpg")\n')
  for topology in topologies:
    for lp in logPoints:
      # one aggregator for each dimension
      #for d in range(dimensions): f.write('d'+str(d) + ' = 0.0\n')
      for run in range(1,runs+1):
        # add variances up for each dimension for each particle
        f.write('g'+str(run)+'_'+str(lp)+'_'+func+' <- read.table("logs/'+topology+'_run'+str(run)+'_populationAt'+str(lp)+'_cg_'+func+'.csv", sep=",", header=FALSE)\n')
        for d in range(dimensions): f.write('d'+str(d) + ' =  g'+str(run)+'_'+str(lp)+'_'+func+'[,'+str(d+1)+']\n')
        f.write('run'+str(run)+'at'+str(lp)+' = mean(c(') # writing an aggregator for one run with the variance in each dimension
        for d in range(dimensions): 
          f.write('var(d'+str(d) + ')')
          if not d == dimensions-1: f.write(',')
        f.write('))\n')
      f.write('agg'+str(lp)+topology+' = mean(c(') # writing an aggregator for one logPoint with the mean run values
      for run in range(1,runs+1): 
        f.write('run'+str(run)+'at'+str(lp))
        if not run == runs: f.write(',')
      f.write('))\n')
    for lp in logPoints: # test output
      f.write('agg'+str(lp)+topology+'\n')
  # open plot - at this time i prefere hard-coded y-axis values (better to compare)  
  #f.write('plot(c(100,200,300),c(')
  #for lp in logPoints:   # take the minimum to arrange the plot  
  #  f.write('min(')
  #  for topology in topologies:
  #    f.write('agg'+str(lp)+topology)
  #    if not topologies.index(topology) == len(topologies)-1: f.write(',')
  #    else: f.write(')')
  #  if not logPoints.index(lp) == len(logPoints)-1: f.write(',') 
  f.write('plot(c(100,200,300,400,500),c(0,3.75,7.5,11.25,15')
  f.write('),type="n",xlab="iteration",ylab="avg. variance per dimension")\n')
  for topology in topologies:
    # write a line through each logpoint
    f.write('lines(c(100,200,300,400,500),lty='+str(topologies.index(topology)+1)+',c(')
    for lp in logPoints: 
      f.write('agg'+str(lp)+topology)
      if not logPoints.index(lp)==len(logPoints)-1: f.write(',')
    f.write('))\n')   
  # write a legend
  f.write('legend('+str(max(logPoints)*0.7)+',')
  #f.write('max(')
  #for topology in topologies: 
  #  f.write('agg'+str(logPoints[0])+topology)
  #  if not topologies.index(topology) == len(topologies)-1: f.write(',')
  #f.write(')*0.3')
  f.write('10')
  f.write(',lty=c(1, 2),legend=c("circle","geographical"))\n')

f.write('dev.off()\n')
f.write('q()\n')
f.close()
