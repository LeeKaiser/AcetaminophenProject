#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 18:12:51 2025

@author: kaiserlee
"""

# Main file for the Acetaminophen Simulation Project

# Import all other files and modules
import numpy as np
import os
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
liver_damage_list = []

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
    liver_damage_list.append(ACE.liver_damage)
    
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
plot_directory = os.path.join(os.getcwd(), ACE.fig_dir)
if ACE.save_plt:
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)

def plot_gen2(list1, list2, list_title_1, list_title_2, title, file_title, xlabel = 'Hours', ylabel = 'mass (mg)'):
    plt.plot(time_steps, list1, label=list_title_1)
    plt.plot(time_steps, list2, label=list_title_2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    if ACE.save_plt: plt.savefig(os.path.join(plot_directory, ACE.fig_title_prefix + file_title))
    plt.show()
    
def plot_gen(list1, list_title_1, title, file_title, xlabel = 'Hours', ylabel = 'mass (mg)'):
    plt.plot(time_steps, list1, label=list_title_1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    if ACE.save_plt: plt.savefig(os.path.join(plot_directory, ACE.fig_title_prefix + file_title))
    plt.show()
    
plot_gen2(blood_ace_list, liver_ace_list, 'blood acetaminophen', 'liver acetaminophen', 'Blood and Liver acetaminophen levels over time', '_Blood_and_Liver_ace.jpg')
plot_gen2(ace_glu_list, ace_sulf_list, 'ace-gluc', 'ace-sulf', 'non toxic metabolites over time', '_non_toxic_metabolites.jpg')
plot_gen2(NAPQI_list, NAPQI_glu_list, 'NAPQI', 'NAPQI-glut', 'NAPQI and NAPQI glut-conjugates over time', '_NAPQI.jpg')
plot_gen2(stomach_ace_list, intest_ace_list, 'stomach acetaminophen', 'intestine acetaminophen', 'digestive system acetaminophen over time', '_digestive_system.jpg')
plot_gen(urine_ace_list,  'urine acetaminophen (mg)',  'urine acetaminophen over time', '_urine_ace.jpg')
plot_gen(liver_damage_list, 'liver damage', 'liver damage over time', '_liver_damage.jpg', ylabel = 'liver damage units')

