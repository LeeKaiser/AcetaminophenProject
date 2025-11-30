#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 12:01:59 2025

@author: kaiserlee
"""

import ace_global_vars as ACE
import numpy as np

ace_in_sys = 0

ace_glu_gen = 0         #   acetaminophen glucuronide generated in last time step
ace_sulf_gen = 0        #   acetaminophen sulfate generated
NAPQI_glu_gen = 0       #   NAPQI glutathione conjugates generated

NAPQI_in_sys = 0        #   NAPQI remaining in system

"""
Time step in liver

input: change in acetaminophen

output: ace_glu and ace_sulf generated, NAPQI generated, ace in system after step
"""
def step(change_in_ace = 0):
    global ace_in_sys, ace_glu_gen, ace_sulf_gen, NAPQI_glu_gen, NAPQI_in_sys
    ace_in_sys += change_in_ace
    print("liver metabolizes acetaminophen to ace_glu, ace_sulf, and NAPQI")
    metabolism()
    print("then NAPQI is detoxified to NAPQI_glu")
    
    return ace_in_sys, ace_glu_gen, ace_sulf_gen, NAPQI_glu_gen, NAPQI_in_sys
    
"""
glu_rate_of_met

return Glucuronidation rate
"""
def glu_rate_of_met():
    liver_drug_con = ace_in_sys / ACE.liver_volume
    glu_max_met = ACE.glu_max_met_rate
    glu_drug_con = ACE.glu_drug_con
    
    return (glu_max_met * liver_drug_con) / (glu_drug_con + liver_drug_con)

"""
glu_rate_of_met

return Sulfation rate
"""
def sulf_rate_of_met():
    liver_drug_con = ace_in_sys / ACE.liver_volume
    sulf_max_met = ACE.sulf_max_met_rate
    sulf_drug_con = ACE.sulf_drug_con
    
    return (sulf_max_met * liver_drug_con) / (sulf_drug_con + liver_drug_con)

"""
metabolism

conduct a time step of metabolism
"""
def metabolism():
    global ace_in_sys, ace_glu_gen, ace_sulf_gen, NAPQI_glu_gen, NAPQI_in_sys
    
    change_in_glu = glu_rate_of_met() * ACE.time_interval
    change_in_sulf = sulf_rate_of_met() * ACE.time_interval
    
    change_in_ace = change_in_glu + change_in_sulf
    
    ace_glu_gen = change_in_glu
    ace_sulf_gen = change_in_sulf
    ace_in_sys -= change_in_ace