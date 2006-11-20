import math

def fitness(particle,conf):
  '''
    When given a particle, fitness() applies its coordinates 
    to the problem and returns a fitness value.
    The functions here are standard problems in evolutionary computation.
    I took them from the paper "Dynamic Sociometry in Particle Swarm Optimization"
    from Richards and Ventura (you can also see pictures of them, 
    of course only two-dimensional )
  '''
  res = 0.0

  if conf.function == 'sphere':      # a good start, maximizes absolute dimension values
    for d in range(conf.dimensions): res += pow(particle.current[d],2)
  elif conf.function == 'rastrigin': # This function has hundreds of steep local optima.
    for d in range(conf.dimensions):
      dim = particle.current[d]
      res += ( pow(dim,2) - 10 * math.cos(2 * math.pi * dim) + 10 )
  elif conf.function == 'griewank': # At a macroscopic level, this function appears very similar to the sphere
                                # function. It does, however, have a very significant amount of noise, so there 
                                # are many deceiving local optima
    tmp = 0.0
    for d in range(conf.dimensions):
      dim = particle.current[d]
      tmp += pow(dim - 100,2)
    one = (( float(1) / float(4000) ) * float(tmp) )
    two = 0.0
    for d in range(conf.dimensions):
      dim = particle.current[d]
      two *= math.cos( (dim - 100)/float(math.sqrt(d+1)) ) + 1
    res = one + two 
  elif conf.function == 'rosenbrock': # ??? TODO: what is this? 
    for d in range(conf.dimensions):
      dim = particle.current[d]
      def getnextdim(particle,dn):
        if dn == conf.dimensions-1: return particle.current[0]
        if dn == conf.dimensions: return particle.current[1]
        else: return particle.current[dn+1]
      nextdim = getnextdim(particle,d)   
      res += ( 100 * (pow(nextdim - pow(dim,2),2)) + pow(dim - 1,2)  )
  else: raise Exception('I do not know the function "' + conf.function + '"!')
  return res 
