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
    

def giveDose():
    global aceInStomach, dosesTaken
    
    mg = ACE.dose_amount * 1000.0
    aceInStomach += mg
    dosesTaken += 1
    
def checkAutoDosing():
    global simTime, dosesTaken
    
    if dosesTaken < ACE.dose_count:
        nextDoseTime = dosesTaken * (ACE.dose_interval * 60)
        if simTime >= nextDoseTime:
            giveDose()


def stomachStep(time):
    global simTime, stomachDoses, intestineDoses, isFed
    
    checkAutoDosing()
    
    if isFed:
        emptyTime = 90
    else:
       emptyTime = 20
        
    remainingStomach = []
    
    for doseTime, amount in stomachDoses:
        timeInStomach = simTime - doseTime
        
        if timeInStomach >= emptyTime:
            intestineDoses.append([simTime, amount])
        else:
            remainingStomach.append([doseTime, amount])
            
    stomachDoses = remainingStomach
    
    simTime += time
    
def intestineStep(time):
    global intestineDoses, simTime, Ka
    
    absorbedTotal = 0.0
    updatedDoses = []
    
    for doseTime, amount in intestineDoses:
        t0 = simTime - doseTime
        t1 = t0 + time
        
        f0 = 1 - np.exp(-Ka * t0)
        f1 = 1 - np.exp(-Ka * t1)
        
        absorbedFraction = f1-f0
        absorbedAmount = amount * absorbedFraction
        absorbedTotal += absorbedAmount
        
        amountRemaining = amount * (1-f1)
        
        if amountRemaining > 1e-6:
            updatedDoses.append([doseTime, amountRemaining])
            
    intestineDoses = updatedDoses
    
    return absorbedTotal
    
    