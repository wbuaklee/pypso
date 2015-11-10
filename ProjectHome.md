This script is an implementation of the Particle Swarm Optimization algorithm in Python.
It's suitable to run experiments on PSO, adjust configuration on the way and with little effort produce graphs.

It was written by Nicolas Hoening (http://www.nicolashoening.de)

Actually, this is more than just the algorithm.
I added a lot of features to play with. For example:
  * Several topologies (circle, star and geographical neighborhood)
  * Some standard functions to test on (sphere,griewank,rastrigin,rosenbrock)
  * Logging capabilities (to csv format, even code to plot graphs with that data in GNU R can be produced)
  * Experiment setups. Average over many iterations and/or automatically change conditions of your choice and let several trials run while you get a fresh cup of coffee :-)

To use it, navigate into the directory where the pypso directory resides, open a Python session and type:
$ import pypso.base
$ pypso.base.run()
(you can also navigate into the pypso directory and leave the "pypso."-parts away)
