#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 18:14:42 2025

@author: kaiserlee
"""

#represents digestive system
import ace_global_vars as ACE
import numpy as np

isFed = False       #whether the individual has fasted or has eaten
stomachDoses = []   #Acetaminophen in the stomach
intestineDoses = [] #Acetaminophen in the intestine
dosesTaken = 0      #doses taken so far
simTime = 0         #simulation time, in minutes
Ka = 2 / 60.0       #absorption constant of ace

"""
takes the amount of time, in minutes, of the step
returns the amount, in milligrams, of the ace being output to the blood during this step
"""
def step(time=30):
    
    stomachStep(time)
    absorbed = intestineStep(time)
    return absorbed
    

"""
administers a dose to the stomach, amount is determined by global vars
"""
def giveDose():
    global stomachDoses, dosesTaken
    
    mg = ACE.dose_amount
    stomachDoses.append([simTime, mg])
    dosesTaken += 1

"""
updates dosing schedule for the next dose to be taken, will administer a dose if it is due
"""
def checkAutoDosing():
    global simTime, dosesTaken
    
    if dosesTaken < ACE.dose_count:
        nextDoseTime = dosesTaken * (ACE.dose_interval * 60)
        if simTime >= nextDoseTime:
            giveDose()

"""
empties the stomach if need be and updates the timers on when doses will be emptied from the stomach
"""
def stomachStep(time):
    global simTime, stomachDoses, intestineDoses, isFed
    
    checkAutoDosing()
    
    #sets the empty time based on if person has eaten or not
    if isFed:
        emptyTime = 90
    else:
       emptyTime = 20
        
    remainingStomach = []
    
    #loops through all doses in stomach
    for doseTime, amount in stomachDoses:
        timeInStomach = simTime - doseTime
        
        #if a dose has spent enough time in stomach, empty to intestine
        if timeInStomach >= emptyTime:
            intestineDoses.append([simTime, amount])
        else:
            #otherwise keep it
            remainingStomach.append([doseTime, amount])
            
    stomachDoses = remainingStomach
    
    simTime += time
    

"""
calculates the absorption of ace into the bloodstream from the intestine
"""
def intestineStep(time):
    global intestineDoses, simTime, Ka
    
    absorbedTotal = 0.0
    updatedDoses = []
    
    #loop through all doses in intestine
    for doseTime, amount in intestineDoses:
        t0 = simTime - doseTime
        t1 = t0 + time
        #t0 time since the dose, t1 is time since t0
        
        #f0 is fraction absorbed already (dose till t0), f1 is fraction absorbed at t1
        f0 = 1 - np.exp(-Ka * t0)
        f1 = 1 - np.exp(-Ka * t1)
        
        #calculate the absorbed fraction, amount, and total
        absorbedFraction = f1-f0
        absorbedAmount = amount * absorbedFraction
        absorbedTotal += absorbedAmount
        
        amountRemaining = amount * (1-f1)
        
        #if there is still some to absorb, keep track of it
        if amountRemaining > 1e-6:
            updatedDoses.append([doseTime, amountRemaining])
            
    intestineDoses = updatedDoses
    
    return absorbedTotal
    
    
    
def get_stomach_amount():
    return sum([amt for _, amt in stomachDoses])

def get_intestine_amount():
    return sum([amt for _, amt in intestineDoses])