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

#These metabolites enter the blood stream instantly
ace_glu_in_sys = 0       #   acetaminophen glucuronide in system
ace_sulf_in_sys = 0      #   acetaminophen sulfate in system
NAPQI_Glu_in_sys = 0     #   NAPQI glutathione conjugates in system

def step():
    print("step in blood stream")