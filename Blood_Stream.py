#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 18:15:15 2025

@author: kaiserlee
"""

#Represents Blood Stream

#Imports
import ace_global_vars as ACE
import numpy as np

#Variables

ace_in_sys = 0           #   Acetaminophen in the system

ace_in_liver = 0        #   known amount of acetaminophen in the liver

#These metabolites enter the blood stream instantly
ace_glu_in_sys = 0       #   acetaminophen glucuronide in system
ace_sulf_in_sys = 0      #   acetaminophen sulfate in system
NAPQI_glu_in_sys = 0     #   NAPQI glutathione conjugates in system

"""
step before liver metabolization
"""
def step_ace_to_liver(absorbedAmount = 0):
    global ace_in_sys
    print("blood stream recieves acetaminophen from digestive system")
    ace_in_sys += absorbedAmount
    print("blood stream sends acetaminophen to liver")
    change = change_in_ace()
    
    
    print("change in ace: ", change, "ace in blood: " , ace_in_sys, "ace in liver: ", ace_in_liver)
    
    return change
    #print("blood stream takes metabolites from liver")
    #print("blood stream sends metabolites to kidneys")
    
    
"""
step after liver metabolization
"""
def step_met_to_kidneys(liver_ace_after_met = 0, new_ace_glu = 0, new_ace_sulf = 0):
    global ace_in_liver, ace_glu_in_sys, ace_sulf_in_sys
    ace_in_liver = liver_ace_after_met
    ace_glu_in_sys += new_ace_glu
    ace_sulf_in_sys += new_ace_sulf
    #print("blood stream takes metabolites from liver")
    #print("blood stream sends metabolites to kidneys")
    
    
"""
returns the change in acetaminophen between blood and liver
"""
def dAldt():
    #get change of acetaminophen in liver over change in time
    blood_volume = 5.0
    A_liver = ace_in_liver
    Q_liver = ACE.liver_blood_flow
    Kp_liver = ACE.ace_partition_coeff
    V_liver = ACE.liver_volume
    
    C_plasma = ace_in_sys / blood_volume
    
    C_blood_equiv_from_liver = A_liver / (Kp_liver * V_liver)
    
    return Q_liver * (C_plasma - C_blood_equiv_from_liver)

"""
get amount of acetaminophen that would be changed within time step.
if the time step is too large, it would be divided into mini steps
with each mini step representing 0.005 hour
"""
def change_in_ace():
    
    global ace_in_sys, ace_in_liver
    total_change = 0
    if ace_in_sys <= 0:
        #skip if there are no acetaminophen
        return 0
    #if time step is too large, then divide it into mini steps to get accurate change
    if ACE.time_interval > 0.01:
        time_mini_steps = np.arange(0,ACE.time_interval, 0.005)
        for i in time_mini_steps:
            change = dAldt() * 0.01
            total_change += change
            ace_in_sys -= change
            ace_in_liver += change
            if ace_in_sys <= 0:
                continue
        
    else:
        #just do 1 step
        total_change += dAldt() * ACE.time_interval
        ace_in_sys -= total_change
    return total_change

