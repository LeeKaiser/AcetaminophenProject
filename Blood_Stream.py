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
import Liver as L

#Variables

ace_in_sys = 100           #   Acetaminophen in the system

#These metabolites enter the blood stream instantly
ace_glu_in_sys = 0       #   acetaminophen glucuronide in system
ace_sulf_in_sys = 0      #   acetaminophen sulfate in system
NAPQI_glu_in_sys = 0     #   NAPQI glutathione conjugates in system

def step_ace_to_liver(absorbedAmount = 0):
    global ace_in_sys
    print("blood stream recieves acetaminophen from digestive system")
    ace_in_sys += absorbedAmount
    print("blood stream sends acetaminophen to liver")
    change = change_in_ace()
    
    
    print("change in ace: ", change, "ace in blood: " , ace_in_sys, "ace in liver: ", L.ace_in_sys)
    #print("blood stream takes metabolites from liver")
    #print("blood stream sends metabolites to kidneys")
    
def dAldt():
    #get change of acetaminophen in liver over change in time
    blood_volume = 5.0
    A_liver = L.ace_in_sys
    Q_liver = ACE.liver_blood_flow
    Kp_liver = ACE.ace_partition_coeff
    V_liver = ACE.liver_volume
    
    C_plasma = ace_in_sys / blood_volume
    
    C_blood_equiv_from_liver = A_liver / (Kp_liver * V_liver)
    
    return Q_liver * (C_plasma - C_blood_equiv_from_liver)

def change_in_ace():
    """get amount of acetaminophen that would be changed within time step, with each mini step representing 1 minute"""
    global ace_in_sys
    total_change = 0
    if ace_in_sys <= 0:
        return 0
    if ACE.time_interval > 0.01:
        time_mini_steps = np.arange(0,ACE.time_interval, 0.01)
        for i in time_mini_steps:
            change = dAldt() * 0.01
            total_change += change
            ace_in_sys -= change
            L.ace_in_sys += change
            if ace_in_sys <= 0:
                continue
            #print(change)
    else:
        total_change += dAldt() * ACE.time_interval
        ace_in_sys -= total_change
    return total_change
    
