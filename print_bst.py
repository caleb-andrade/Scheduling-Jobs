# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 18:41:13 2015

@author: Caleb Andrade
"""

from Tkinter import Tk
from Tkinter import Canvas
from math import floor as flr
from math import log

def print_bst(job_bst, yrange, boxes, eq, eq_intsc):
    """
    prints the solution given by the sweep-greedy algorithm, normalizing the
    drawing to the unit square. Jobs will be displayed as vertical segments,
    and a graphical visualization of the objective function will be given 
    by displaying boxes of "area contributions"
    """
    root = Tk()
    canvas = Canvas(root, width = 600, height = 630, background = "white")
    canvas.pack()
    for box in boxes[0]:
        d = box[2] - box[0]            
        box_color = "#%02x%02x%02x" % (int(255*(0.5-d)), int(255*(0.75-d)), int(255*(1-d)))
        canvas.create_rectangle(box[0]*600, 630 - box[1]*600/yrange,
                                box[2]*600, 630 - box[3]*600/yrange, 
                                fill= box_color, dash = 1)
    avg = opt_area_bound(eq, eq_intsc)
    apx = boxes[1]
    ravg = round(avg/yrange, 3)
    rapx = round(apx/yrange, 3)
    ratio = "       " + str(round(apx / avg, 3)) + " < Apx factor"
    info =  "Apx = " + str(rapx) + " < OPT < Avg = " + str(ravg) + ratio
    canvas.create_text((300, 15), text = info, font = ("Helvetica", 15))
    job_color = "#%02x%02x%02x" %(255, 0, 0)
    for idx in range(len(job_bst)):
        dya = dyadic(idx + 1)
        for job in job_bst[idx]:
            canvas.create_line(dya*600, 630 - job.start*600/yrange, 
                               dya*600, 630 - job.end*600/yrange, 
                               fill = job_color, width = 2)
    root.mainloop()

def dyadic(n):
    """
    calculates the dyadic position for the nth node(BFS) of the BST
    """
    return (1 + 2*(n - 2**(flr(log(n, 2))))) / 1/2**(flr(log(n, 2)) + 1)
    
    
def area_boxes(idx_bst, eq, eq_intsc):
    """
    calculates the "minimum boxes" and the area of the solution given by
    the sweep-greedy algorithm
    """
    boxes = []    
    area = 0
    for idx in range(len(eq) - 1):
        event_kset = eq_intsc[eq[idx]].copy()
        node_num = 0        
        for node in idx_bst[0:]:
            event_kset.difference_update(node)
            node_num = idx_bst.index(node)
            if len(event_kset) == 0:
                break
        dmin = 1 / 2**(flr(log(node_num + 1, 2)) + 1)
        boxes.append((0, eq[idx], dmin, eq[idx + 1]))
        area += dmin*(eq[idx + 1] - eq[idx])
    #print "\nBOXES: ", boxes
    print "\nAREA OF APX: ", area
    return boxes, area
    
def opt_area_bound(eq, eq_intsc):
    """
    calculates the upper bound for the optimal area
    """
    area = 0
    for idx in range(len(eq) - 1):
        event_kset = eq_intsc[eq[idx]]
        k = len(event_kset)
        area += float(eq[idx + 1] - eq[idx]) / (k + 1)
    print "\nAREA UPPER BOUND FOR OPT: ", area
    return area
        
        
    
            
            
            
                    
                
   
       
    
    

