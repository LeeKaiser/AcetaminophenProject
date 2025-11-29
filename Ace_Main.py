#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 18:12:51 2025

@author: kaiserlee
"""

# Main file for the Acetaminophen Simulation Project

# Import all other files and modules
import numpy as np
import ace_global_vars as ACE
import Digestive_System as DS
import Blood_Stream as BS

# Initialize constant variables
time = ACE.time                   #   amount of time in simulation
time_interval = ACE.time_interval        #   amount of time passed per interval (total time steps = time/time_interval)


# 

#initialize all time steps
time_steps = np.arange(0,time,time_interval)

#iterate through each time step to run parts of simulation
for i in time_steps:
    print("T: " , i)
    Ace_to_blood = DS.step(60 * time_interval)
    Ace_to_liver = BS.step_ace_to_liver(Ace_to_blood)
