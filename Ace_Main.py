#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 18:12:51 2025

@author: kaiserlee
"""

# Main file for the Acetaminophen Simulation Project

# Import all other files and modules
import numpy as np
import numpy.ma as ma
import ace_global_vars as ACE
import Digestive_System as DS
import Blood_Stream as BS
import Kidneys as K
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
urine_vol_list = []
urine_ace_list = []
urine_ace_glu_list = []
urine_ace_sulf_list = []
urine_NAPQI_glu_list = []

#iterate through each time step to run parts of simulation
for i in time_steps:
    #print("T: " , i)
    # run all step methods
    ace_to_blood = DS.step(60 * time_interval)
    ace_to_liver = BS.step_ace_to_liver(ace_to_blood)
    ace_in_liv, ace_glu_gen, ace_sulf_gen, NAPQI_glu_gen, NAPQI_in_liv = L.step(ace_to_liver)
    
    BS.step_met_to_kidneys(ace_in_liv, ace_glu_gen, ace_sulf_gen, NAPQI_glu_gen)
    kidney_out = K.step(60 * time_interval)
    
    #append all values being kept track of
    blood_ace_list.append(BS.ace_in_sys)
    liver_ace_list.append(ace_in_liv)
    ace_glu_list.append(BS.ace_glu_in_sys)
    ace_sulf_list.append(BS.ace_sulf_in_sys)
    NAPQI_list.append(NAPQI_in_liv)
    NAPQI_glu_list.append(BS.NAPQI_glu_in_sys)
    stomach_ace_list.append(DS.get_stomach_amount())
    intest_ace_list.append(DS.get_intestine_amount())
    urine_vol_list.append(K.urine_volume_list[-1])
    urine_ace_list.append(sum(K.urine_ace_list))
    
#convert to masked array
blood_ace_list = ma.masked_equal(np.array(blood_ace_list), 0)
intest_ace_list = ma.masked_equal(np.array(intest_ace_list), 0)
stomach_ace_list = ma.masked_equal(np.array(stomach_ace_list), 0)
liver_ace_list = ma.masked_equal(np.array(liver_ace_list), 0)
ace_glu_list = ma.masked_equal(np.array(ace_glu_list), 0)
ace_sulf_list = ma.masked_equal(np.array(ace_sulf_list), 0)
NAPQI_glu_list = ma.masked_equal(np.array(NAPQI_glu_list), 0)
NAPQI_list = ma.masked_equal(np.array(NAPQI_list), 0)
urine_ace_list = ma.masked_equal(np.array(urine_ace_list), 0)

#generate plots


plt.plot(time_steps, blood_ace_list, label='blood acetaminophen')
plt.plot(time_steps, liver_ace_list, label='liver acetaminophen')
plt.legend()

plt.show()

plt.plot(time_steps, ace_glu_list, label='ace-glu')
plt.plot(time_steps, ace_sulf_list, label='ace-sulf')

plt.legend()

plt.show()

plt.plot(time_steps, NAPQI_list, label='NAPQI')
plt.plot(time_steps, NAPQI_glu_list, label='NAPQI-glu')
plt.legend()

plt.show()

plt.plot(time_steps, stomach_ace_list, label='stomach acetaminophen')
plt.plot(time_steps, intest_ace_list, label='intestine acetaminophen')
plt.legend()
plt.show()

plt.plot(time_steps, urine_ace_list, label='urine acetaminophen (mg)')
plt.legend()
plt.show()