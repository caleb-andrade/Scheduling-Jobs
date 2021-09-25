# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 11:20:53 2015

@author: Caleb Andrade
"""

import Interval as Int
from Tkinter import Tk
from Tkinter import Canvas
from math import exp
import time
import random

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************
def jobsEq(joblist):
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
    jobs.sort() 
    jobs = tuple(jobs)
    
    arrivals = [job.start for job in jobs]
    departures = [job.end for job in jobs]
    eq = list(set(arrivals + departures))
    eq.sort() 
    eq = tuple(eq) 

    return jobs, eq

def jobsEqDict(jobs, eq):
    """
    Returns 'eq_dict', a dictionary where keys are events in EQ and their 
    values are those jobs that contain such event (except as endpoint). In
    the same way, a second dictionary 'job_dict' is created where keys are
    jobs and their values those events spanned by the job as key.
    """
    eq_dict = {idx:set([]) for idx in range(len(eq) - 1)} 
    job_dict = {idx:set([]) for idx in range(len(jobs))}
    for event in eq:
        for idx in range(len(jobs)):
            if jobs[idx].__contains__(event):
                jdx = eq.index(event)
                eq_dict[jdx].add(idx)
                job_dict[idx].add(jdx)
            elif (event < jobs[idx].start): # lexicographic order in action
                break
    
    return job_dict, eq_dict

def readFile(filetxt):
    """
    Reads a file that has stored ordered pairs of numbers separated by space 
    in a single string, returns 'joblist'.
    """
    f = open(filetxt, 'r')
    joblist = []
    temp = []
    for read in f.readline().split():
        temp.append(float(read))
        if len(temp) == 2:
            joblist.append(tuple(temp))
            temp = []
    return joblist
    

#******************************************************************************
# JOB SCHEDULING CLASS OBJECT
#******************************************************************************
class Jobs(object):
    """
    Description.
    """
    def __init__(self, joblist, interval):
        """
        Initializing.
        """
        jobs, eq = jobsEq(joblist)
        job_dict, eq_dict = jobsEqDict(jobs, eq)
        self.jobs = jobs
        self.eq = eq
        self.job_dict = job_dict
        self.eq_dict = eq_dict
        self.locations = {idx:0 for idx in range(len(jobs))}
        self.a = interval[0]
        self.b = interval[1]
        self.min_distances = [0 for idx in range(len(eq) - 1)]
        self.objective_value = 0
        self.n = len(jobs)
        self.boxes = {}
        self.max_overlaps = []
        
        for job in range(len(jobs)):
            max_overlap = 0
            for event in job_dict[job]:
                if len(eq_dict[event]) > max_overlap:
                    max_overlap = len(eq_dict[event])
            self.max_overlaps.append(max_overlap)
        
    def __str__(self):
        """
        As string.
        """
        string = ""
        for idx in range(len(self.jobs)):
            string += "\nJob " + str(idx) + ": " + str(self.jobs[idx])
            string += " Location: " + str(self.locations[idx])
        return string
        
    def getJobs(self):
        """
        Returns a list of the jobs.
        """
        return list(self.jobs)
        
    def getEq(self):
        """
        Returns a list of the event queue.
        """
        return list(self.eq)
        
    def getJobsLoc(self):
        """
        Returns a list of tuples: (job, location).
        """
        temp = []
        for idx in range(len(self.jobs)):
            temp.append((self.jobs[idx], self.locations[idx]))
        return temp
        
    def getObjValue(self):
        """
        Returns objective value. The sum over all sections of the minimum area 
        enclosed at each section.
        """
        return self.objective_value
        
    def getJobArea(self, job):
        """
        Returns the area contribution of those sections spanned by job.
        """
        area = 0
        for event in self.job_dict[job]:
            area += (self.eq[event + 1] - self.eq[event])*self.minDist(event)
        return area            
        
    def setJobLoc(self, job, value):
        """
        Places 'job' at location 'value' in the interval (a,b).
        """
        if job < 0 or job > self.n:
            raise ValueError('Invalid job!')
        if value <= self.a or self.b <= value:
            raise ValueError('Invalid location!')
        temp = self.getJobArea(job)
        self.locations[job] = value
        # update objective value and min_distances
        self.updateMinDist(job)
        self.objective_value += self.getJobArea(job) - temp
        
    def getBoxes(self):
        """
        Constructs and returns the boxes that represent the min area in each
        section.
        """
        boxes = []
        for idx in self.boxes.keys():
            boxes.append((self.boxes[idx][0], self.eq[idx],
                          self.boxes[idx][1], self.eq[idx + 1]))
        return boxes
        
    def minDist(self, event):
        """
        Calculates the minimum distance between jobs' locations
        at section defined by 'event'. A section is defined as the 
        interval defined by two consecutive events, the start point 
        of the interval is the event of reference for such section.
        """
        job_loc = []
        for job in self.eq_dict[event]:
            job_loc.append(self.locations[job])
        job_loc.sort()

        min_dist = self.b - self.a
        # loop through jobs' locations sorted in increasing order
        for idx in range(len(job_loc) - 1):
            dist = job_loc[idx + 1] - job_loc[idx]
            if dist < min_dist:
                min_dist = dist
                self.boxes[event] = (job_loc[idx], job_loc[idx + 1])
        # two corner cases at endpoints of (a,b)
        if job_loc[0] - self.a < min_dist:
            min_dist = job_loc[0] - self.a
            self.boxes[event] = (self.a, job_loc[0])
        if self.b - job_loc[-1] < min_dist:
            min_dist = self.b - job_loc[-1]
            self.boxes[event] = (job_loc[-1], self.b)
            
        return min_dist
        
    def updateMinDist(self, job):
        """
        Updates minimum distances at sections spanned by job.
        """
        for event in self.job_dict[job]:
            self.min_distances[event] = self.minDist(event)
            
    def draw(self):
        """
        Draws jobs, normalizing to the unit square. It also shades the area
        contribution to the objective value at each section.
        """
        yrange = self.eq[-1] - self.eq[0]
        root = Tk()
        canvas = Canvas(root, width = 600, height = 630, background = "white")
        canvas.pack()
        for box in self.getBoxes():
            d = box[2] - box[0]            
            box_color = "#%02x%02x%02x" % (int(255*(0.5-d)), int(255*(0.75-d)), int(255*(1-d)))
            canvas.create_rectangle(box[0]*600, 630 - box[1]*600/yrange,
                                    box[2]*600, 630 - box[3]*600/yrange, 
                                    fill= box_color, dash = 1)
        
        info =  "Objective Value: " + str(self.objective_value)
        canvas.create_text((300, 15), text = info, font = ("Helvetica", 15))
        job_color = "#%02x%02x%02x" %(255, 0, 0)
        for item in self.getJobsLoc():
            job = item[0]
            location = item[1]
            canvas.create_line(location*600, 630 - job.start*600/yrange,
                               location*600, 630 - job.end*600/yrange, 
                                   fill = job_color, width = 2)
        root.mainloop()

#******************************************************************************
# SIMULATED ANNEALING
#******************************************************************************
def simAnnealing(jobs, temperature, mkv_long, cooling_factor, rangen = True):
    """
    Basic implementation of simulated annealing.
    """
    if rangen:
        initialSol(jobs)
    obj_val = jobs.getObjValue() # objective value
    histogram = [obj_val]
    
    tic = time.clock()
    # start simulation
    while temperature > 0.01: # stopping condition!
        count = 0
        # markov chain loop, before decreasing temperature
        while count < mkv_long:
            # loop through every job
            for job in range(jobs.n):
                # propose a feasible relocation
                temp_loc = jobs.locations[job]
                feasibleLoc(job, jobs)
                temp_obj_val = jobs.getObjValue()
                accept = False
                # determine if relocation is accepted
                if temp_obj_val >= obj_val:
                    accept = True
                else:
                    prob = 1 / exp((obj_val - temp_obj_val) / temperature)
                    if random.random() <= prob:
                        accept = True
                if accept:
                    obj_val = temp_obj_val
                    histogram.append(obj_val)
                    count += 1
                else:
                    jobs.setJobLoc(job, temp_loc)
        temperature = cooling_factor*temperature
    toc = time.clock()
        
    jobs.draw()
    print "\nRunning time: ", toc-tic
    print "Objective value: ", jobs.getObjValue()
    
    return histogram
    
def feasibleLoc(job, jobs):
    """
    Relocates job to a feasible relocation, using a uniform random dist.
    """
    location = jobs.locations[job]
    feasible = False
    while not feasible:
        # slack is bounded by 1/m+1, where m is the max
        # number of overlaps of 'job' with other jobs
        slack = random.uniform(-1, 1) / (1 + jobs.max_overlaps[job])
        new_location = location + slack
        if new_location > jobs.a and new_location < jobs.b:
            feasible = True
    jobs.setJobLoc(job, new_location)
    
def initialSol(jobs):
    """
    Sets a initial solution by placing randomly each job in (a,b) uniformly.
    """
    for job in range(jobs.n):
        jobs.setJobLoc(job, jobs.a + jobs.b*random.random())
    print "\nInitial solution: "   
    print "\nInitial objective value: ", jobs.getObjValue() 
    print jobs
    
    jobs.draw()
    
           
                    
                
        
        
        
            
    
        
              
        
    

    