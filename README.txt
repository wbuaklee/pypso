################################################################################
#  ----------- PyPSO -----------
#  
#  This script is an implementation of the Particle Swarm Optimization
#  algorithm in Python.
#  It can be used to perform basic experiments with PSO.
#  It was written by Nicolas Hoening (http://www.nicolashoening.de)
#  with some inspiration by pseudocode of adaptiveview.com:
#  http://www.adaptiveview.com/articles/ipsop1.html 
# 
#  Actually, this is more than just the algorithm.
#  I added a lot of features to play with. For example:
#  - Several topologies (circle, star and geographical neighborhood)
#  - Some standard functions to test on (sphere,griewank,rastrigin,rosenbrock)
#  - Logging capabilities (to csv format, even code to plot graphs with that in GNU R can be produced)
#  - Experiment setups. Average over many iterations and/or automatically change conditions of your 
#      choice and let several trials run while you get a fresh cup of coffee :-)
#
#  To use it, navigate into the directory where the pypso directory resides, 
#  open a Python session and type:
#  $ import pypso.base
#  $ pypso.base.run()
#  (you can also navigate into the pypso directory and leave the "pypso."-parts away in the 
#  python-session) 
#
#  There are a lot of things to tweak with in the file conf.py.
#
#  If you have comments and/or help, feel free to drop me a line at nhoening [at] gmail [dot] com 
#
#  -------- GNU Licence -------
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA'
################################################################################
