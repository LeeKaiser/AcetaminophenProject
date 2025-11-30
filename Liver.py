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
returns p450 processing rate
"""
def p450_rate_of_met():
    liver_drug_con = ace_in_sys /ACE.liver_volume
    p450_max = ACE.p450_max_met_rate
    p450_km = ACE.p450_drug_con
    return (p450_max * liver_drug_con) / (p450_km + liver_drug_con)

"""
returns detoxification rate of NAPQI
"""
def detox_rate_of_NAPQI():
    if ACE.GSH_amount <= ACE.GSH_baseline * ACE.GSH_min_threshold:
        return 0.0
    
    GSH_con = ACE.GSH_amount
    GSH_km = ACE.GSH_km
    detox_max = ACE.NAPQI_detox_max_rate
    
    rate = (detox_max * GSH_con) / (GSH_km + GSH_con)
    
    return min(rate, NAPQI_in_sys / ACE.liver_volume)

"""
metabolism

conduct a time step of metabolism
"""
def metabolism():
    global ace_in_sys, ace_glu_gen, ace_sulf_gen, NAPQI_glu_gen, NAPQI_in_sys
    
    change_in_glu = glu_rate_of_met() * ACE.time_interval
    change_in_sulf = sulf_rate_of_met() * ACE.time_interval
    change_in_p450 = p450_rate_of_met() * ACE.time_interval
    
    
    change_in_ace = change_in_glu + change_in_sulf + change_in_p450
    
    
    ace_glu_gen = change_in_glu
    ace_sulf_gen = change_in_sulf
    NAPQI_in_sys += change_in_p450
    ace_in_sys -= change_in_ace
    ace_in_sys = max(0, ace_in_sys)
    
    detox_rate = detox_rate_of_NAPQI() * ACE.time_interval
    NAPQI_glu_gen = detox_rate
    
    NAPQI_in_sys -= detox_rate
    NAPQI_in_sys = max(0, NAPQI_in_sys)
    
    if detox_rate > 0:
        ACE.GSH_amount -= detox_rate
        ACE.GSH_amount = max(0, ACE.GSH_amount)