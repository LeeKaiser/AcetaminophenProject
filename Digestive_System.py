#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 18:14:42 2025

@author: kaiserlee
"""

#represents digestive system
import ace_global_vars as ACE
import numpy as np
#import Ace_Main as main

isFed = False       #whether the individual has fasted or has eaten
aceInStomach = 0    #Acetaminophen in the stomach
aceInIntestine = 0  #Acetaminophen in the intestine
lastDose = 0        #time since last dose, in minutes
dosesTaken = 0      #doses taken so far
#simTime = 0         #simulation time, in minutes

"""
takes the amount of time, in minutes, of the step
returns the amount, in milligrams, of the ace being output to the blood during this step
"""
def step(time=30):
    #global simTime
    
    stomachStep(time)
    intestineStep(time)
    #simTime += time
    
    print("step in digestive system done")
    

def stomachStep(time):
    global lastDose
    global aceInIntestine
    global aceInStomach
    #global simTime
    global dosesTaken
    
    if dosesTaken < ACE.dose_count and lastDose == ACE.dose_interval:
        aceInStomach += (ACE.dose_amount) * 1000
        lastDose = 0
        dosesTaken += 1
    
    if not isFed:
        if lastDose > 20:
            aceInIntestine += aceInStomach
            aceInStomach = 0
        else:
            lastDose += time
        
    else:
        if lastDose > 90:
            aceInIntestine += aceInStomach
            aceInStomach = 0
        else:
            lastDose += time
    print("step in stomach done")
    
def intestineStep(time):
    print("step in intestine done")