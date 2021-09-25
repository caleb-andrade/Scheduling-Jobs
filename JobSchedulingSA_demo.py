"""
Created on Sun Nov 01 13:01:43 2015

@author: Caleb Andrade
"""

import JobSchedulingSA as js
from matplotlib import pyplot as plt

joblist = js.readFile('example.txt')

# Testing Simulated Annealing
jobs = js.Jobs(joblist, (0,1))
histogram = js.simAnnealing(jobs, 1, 5000, 0.5)
plt.plot(histogram)
plt.show()
print "Final Solution: \n", jobs




