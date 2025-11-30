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
import Liver as L
import matplotlib.pyplot as plt

# Initialize constant variables
time = ACE.time                   #   amount of time in simulation
time_interval = ACE.time_interval        #   amount of time passed per interval (total time steps = time/time_interval)


# 

#initialize all time steps
time_steps = np.arange(0,time,time_interval)

#initialize lists containing info on amount of chemicals at each step
stomach_ace_list = []
intest_ace_list = []
blood_ace_list = []
liver_ace_list = []
ace_glu_list = []
ace_sulf_list = []
NAPQI_list = []
NAPQI_glu_list = []

#iterate through each time step to run parts of simulation
for i in time_steps:
    print("T: " , i)
    ace_to_blood = DS.step(60 * time_interval)
    ace_to_liver = BS.step_ace_to_liver(ace_to_blood)
    ace_in_liv, ace_glu_gen, ace_sulf_gen, NAPQI_glu_gen, NAPQI_in_liv = L.step(ace_to_liver)
    
    BS.step_met_to_kidneys(ace_in_liv, ace_glu_gen, ace_sulf_gen)
    
    #append all values being kept track of
    blood_ace_list.append(BS.ace_in_sys)
    liver_ace_list.append(ace_in_liv)
    ace_glu_list.append(BS.ace_glu_in_sys)
    ace_sulf_list.append(BS.ace_sulf_in_sys)
    
plt.plot(time_steps, blood_ace_list, label='blood acetaminophen')
plt.plot(time_steps, liver_ace_list, label='liver acetaminophen')
plt.plot(time_steps, ace_glu_list, label='ace-glu')
plt.plot(time_steps, ace_sulf_list, label='ace-sulf')
plt.legend()

plt.show()