# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 20:29:35 2015

@author: Caleb Andrade
"""

import Interval as Int
from math import floor as flr
from math import log
import random

#*****************************************************************************
# HELPER FUNCTIONS
#*****************************************************************************

# Helper function that builds the list of jobs and creates the event queue EQ
def jobs_eq(joblist):
    """
    Takes as argument a list of tuples 'joblist', converting tuples into 
    interval objects, storing and sorting them lexicographically in a list.
    It also creates EQ. Returns 'jobs' and 'eq' as immutable data types.
    """
    jobs = []
    for job in joblist:
        if job[0] == job[1]:
            print "Not a valid job! will be discarded!"
        else:
            jobs.append(Int.Interval(job[0], job[1]))
    jobs.sort() # sort jobs lexicographically
    jobs = tuple(jobs) # converting to a immutable data type
    #print "\nSORTED JOBS: ", jobs
        
    arrivals = [job.start for job in jobs]
    departures = [job.end for job in jobs]
    eq = list(set(arrivals + departures))
    eq.sort() # create EQ without duplicates, sort it
    eq = tuple(eq) # converting to a immutable data type
    #print "\nEQ: ", eq
    
    return jobs, eq

# Helper function that computes the sets of jobs that intersect between events
def eq_intersections(eq, jobs):
    """
    Takes as argument EQ and the list of sorted jobs. An event e_i is 
    associated with the interval defined by (e_i, e_i+1). A dictionary is 
    created 'eq_intsc' where keys are events and their values the a set of jobs 
    spanning the respective event's interval. Returns also the max of section 
    type 'maxsec'
    """
    eq_intsc = {event:set([]) for event in eq} 
    maxsec = count = 0 
    for event in eq:
        if count > maxsec:
            maxsec = count
        count = 0
        for idx in range(len(jobs)):
            if jobs[idx].__contains__(event):
                eq_intsc[event].add(idx)
                count += 1
            elif (event < jobs[idx].start):
                break
    #print "\nEQ_INTERSECTIONS: ", eq_intsc
    return eq_intsc, maxsec

# Helper function that determines intersections among jobs
def job_intersections(jobs):
    """
    For every job it stores the set of its overlapping jobs in a dictionary
    """
    jo_intsc = {i:set([]) for i in range(len(jobs))}
    for job in range(len(jobs)):
        for idx in range(len(jobs)):
            if jobs[job].overlap(jobs[idx]) and job != idx:
                jo_intsc[job].add(idx)                    
            elif(jobs[job].end < jobs[idx].start):
                break
    #print "\nJOB INTERSECTIONS: ", jo_intsc
    return jo_intsc
    
# Lets build a function for the sweep stage to preprocess data
def sweep_line(joblist):
    """
    Takes as argument a list of intervals 'joblist' and returns the matrix 
    of area contributions (rows = jobs; cols = contribution per section type).
    A section refers to the interval between two consecutive events, its type
    is defined by the number of jobs that intersect with it
    """
    jobs, eq = jobs_eq(joblist)    
    eq_intsc, m = eq_intersections(eq, jobs)
    
    if m == 0: return []
    area_matrix = [[0 for j in range(m)] for i in range(len(jobs))]
        
    for idx in range(len(eq) - 1):
        k = len(eq_intsc[eq[idx]]) # section type
        delta = eq[idx + 1] - eq[idx] # size of eq's interval
        for job in eq_intsc[eq[idx]]:
            area_matrix[job][k - 1] += delta /2**(flr(log(k,2)) + 1)
   
    #print "\nAREA MATRIX: "
    #for row in area_matrix:
    #     print row
    
    return area_matrix, jobs, eq, eq_intsc, m
    
def job_priority(a_m):
    """
    Takes as argument the area_matrix and constructs a PQ, where the priority
    of a job is the order defined by: (section type, 1 / max_cont) in a
    lexicographical fashion. According to this priority, jobs will be processed
    into the BST to define its location on the unit interval
    """
    pq = []
    if len(a_m) == 0: 
        return pq
    for job in range(len(a_m)):
        champ = 0
        for idx in range(len(a_m[job])):
            if a_m[job][idx] > a_m[job][champ]:
                champ = idx
        pq.append((champ, 1 / a_m[job][champ], job))
    pq.sort()
    #print "\nJOBS PRIORITY QUEUE: ", job_pq
    job_pq = tuple([pq[i][2] for i in range(len(pq))])
    #print "\nPRIORITY QUEUE INDEXES OF JOBS: ", job_pq
    return job_pq
            
def bst_location(job_pq, jobs):
    """
    Defines the location of jobs in the unit interval by processing them
    according to a PQ in a BFS fashion. When a job is to be inserted it 
    searches the BST until it finds an available node, by this we mean that
    either is empty or the jobs stored at that node do not overlap with it.
    The nodes in the BST have a bijective correspondence with dyadic points.
    """
    idx_bst = [set([])]
    jo_intsc = job_intersections(jobs)
    
    for job in job_pq:
        for node in idx_bst:
            if len(node) == 0:
                node.add(job)
                idx_bst.append(set([]))
                break
            if len(node.intersection(jo_intsc[job])) == 0:
                node.add(job)
                break
    if len(idx_bst[-1]) == 0: idx_bst.pop()
    #print "\nBST FOR JOBS: ", idx_bst
    job_bst = [set([]) for i in range(len(idx_bst))]
    for i in range(len(idx_bst)):
        for j in idx_bst[i]:
            job_bst[i].add(jobs[j])
    return job_bst, idx_bst
                
def random_jobs(n):
    """
    generates a list with n random jobs over the unit interval
    """
    jobs = []
    for i in range(n):
        x1 = random.random()
        x2 = random.random()
        jobs.append((min(x1, x2), max(x1, x2)))
    return jobs
        
        
    
    
            
            
            
        
    
    
    
    
    
             
    
    
