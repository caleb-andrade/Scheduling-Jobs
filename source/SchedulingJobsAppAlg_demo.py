"""
Created on Tue Sep 08 09:14:29 2015

@author: Caleb Andrade
"""

import SchedulingJobsAppAlg as sj
import print_bst as pbst
import time

def run_example(ex):
    """
    does what it says! takes as argument a list of jobs (intervals)
    """
    tic = time.clock()
    info = sj.sweep_line(ex)
    am = info[0]                   # area matrix
    jobs = info[1]                 # list of jobs as intervals
    eq = info[2]                   # event queue EQ
    eq_intsc = info[3]             # intersections at each section
    job_pq = sj.job_priority(am)   # preprocessed jobs in a priority queue
    job_bst, idx_bst = sj.bst_location(job_pq, jobs) # jobs locations in bst
    boxes = pbst.area_boxes(idx_bst, eq, eq_intsc)
    toc = time.clock()
    pbst.print_bst(job_bst, eq[-1], boxes, eq, eq_intsc) # lets draw!
    print "\nRunning time: ", toc - tic
    
def random_example(lo, hi):
    """
    generates a random set of n jobs (in the unit interval), where n is a 
    random variable in (lo, hi)
    """
    print "\n------------------------RANDOM EXAMPLE----------------------------"
    f = open("random_example.txt", 'w')    
    ex1 = sj.random_jobs(sj.random.randint(lo, hi))
    for job in ex1:
        f.write(str(job[0]) + " " + str(job[1]) + " ")
    f.close()
    run_example(ex1)
    
def read_example(filetxt):
    """
    reads a file that has stored ordered pairs of numbers separated by space 
    in a single string. Those pairs are jobs.
    """
    f = open(filetxt, 'r')
    ex = []
    temp = []
    for x in f.readline().split():
        temp.append(float(x))
        if len(temp) == 2:
            ex.append(tuple(temp))
            temp = []
    return ex

# Random example
print "\nSpecify the range (Lo, Hi) to generate a random number for number of jobs"
lo = int(input("Lo: "))
hi = int(input("Hi: "))

print "\nTo save this example, rename the file 'random_example.txt' in"
print "the folder where this binary file is located"
random_example(lo, hi)

         
#*****************************************************************************
#                                  E X A M P L E S
#*****************************************************************************

print "\n------------------------------EXAMPLE 1----------------------------"
ex1 = [(0,4), (2,8),(2,8),(6,14),(6,14),(10,14),(12,20),(12,20),
       (12,16),(12,16),(18,24),(18,24),(22,26)]
run_example(ex1)

#print "\n------------------------------EXAMPLE 2----------------------------"
#ex2 = [(4, 5), (3, 4), (2, 3), (1, 2), (0, 1)]
#run_example(ex2)

#print "\n------------------------------EXAMPLE 3----------------------------"
#ex3 = [(0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1)]
#run_example(ex3)

#print "\n------------------------------EXAMPLE 4----------------------------"
#ex4 = [(0, 0), (0, 1)]
#run_example(ex4)

#print "\n------------------------------EXAMPLE 5----------------------------"
#ex5 = [(2, 2.5), (1.5, 2), (1, 1.5), (0.5, 1), (0, 0.5)]
#run_example(ex5)

#print "\n------------------------------EXAMPLE 6----------------------------"
#ex6 = [(4, 5.5), (3, 4.5), (2, 3.5), (1, 2.5), (0, 1.5)]
#run_example(ex6)

#print "\n------------------------------EXAMPLE 7----------------------------"
#ex7 = [(0, 6), (5, 6), (5, 6), (5, 6), (5, 6), (5, 6), (5, 11)]
##run_example(ex7)

#print "\n------------------------------EXAMPLE 8----------------------------"
#ex8 = [(12, 15), (10, 13), (8, 11), (6, 9), (2, 6), (0, 3)]
#run_example(ex8)

#print "\n------------------------------EXAMPLE 9----------------------------"
#ex9 = [(0, 12), (1, 13), (2, 14), (3, 15), (4, 16), 
#       (5, 17), (6, 18), (7, 60)]
#run_example(ex9)

#print "\n-----------------------------EXAMPLE 10----------------------------"
#ex10 = [(0,5), (3, 12), (3, 12), (3, 16)]
#run_example(ex10)
