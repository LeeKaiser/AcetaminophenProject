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
    change_in_ace = dQldt() * ACE.time_interval
    L.ace_in_sys += change_in_ace
    ace_in_sys -= change_in_ace
    print("change in ace: ", change_in_ace, "ace in blood: " , ace_in_sys, "ace in liver: ", L.ace_in_sys)
    print("blood stream takes metabolites from liver")
    print("blood stream sends metabolites to kidneys")
    
def dQldt():
    #get change of acetaminophen in liver over change in time
    Qliver = L.ace_in_sys               #amount of drug in liver
    Fliver = ACE.liver_blood_flow       #blood flow rate to liver
    Cace = ace_in_sys * 0.15 / ACE.liver_blood_volume    #concentration of drug in blood supplying the liver in mg/L
    Pliver = ACE.ace_partition_coeff    #blood partition coefficient
    Vliver = ACE.liver_volume           #volume of tissue in liver
    
    return (Fliver) * (Cace - (Qliver / (Pliver * Vliver)))
