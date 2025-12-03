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
    #print("liver metabolizes acetaminophen to ace_glu, ace_sulf, and NAPQI")
    metabolism()
    ethanol_clearance()
    regen_gsh()
    update_hepatocyte_viability()
    #print("then NAPQI is detoxified to NAPQI_glu")
    
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
    
    E = ACE.ethanol_amount
    induction = 1.0 + ACE.ethanol_induction_factor * (E / (ACE.ethanol_induction_k + E)) if E > 0 else 1.0
    
    base_rate = (p450_max * liver_drug_con) / (p450_km + liver_drug_con)
    
    return base_rate * induction

"""
returns detoxification rate of NAPQI
"""
def detox_rate_of_NAPQI():
    global NAPQI_in_sys
    
    E = ACE.ethanol_amount
    
    ethanol_compete = ACE.ethanol_GSH_compete * (E / (ACE.ethanol_induction_k + E)) if E > 0 else 0.0
    
    effective_GSH = max(0.0, ACE.GSH_amount - ethanol_compete)
    
    if effective_GSH <= ACE.GSH_baseline * ACE.GSH_min_threshold:
        return 0.0
    
    GSH_con = effective_GSH
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
        
    residual_conc = NAPQI_in_sys / ACE.liver_volume
    
    threshold = ACE.NAPQI_toxic_threshold
    if residual_conc > threshold:
        excess = (residual_conc - threshold) / max(threshold, 1e-12)
        normalized_excess = excess ** ACE.damage_exponent
        
        
        gsh_protection = 1.0
        
        if ACE.GSH_amount <= ACE.GSH_baseline * ACE.GSH_min_threshold:
            gsh_protection = 2.0

        damage_rate = ACE.toxicity_constant * normalized_excess * gsh_protection
        damage_increment = max(ACE.min_damage_increment, damage_rate * ACE.time_interval)
        ACE.liver_damage += damage_increment
    
    
    ACE.liver_damage = max(0.0, ACE.liver_damage)
    
    repair = ACE.liver_repair_rate * ACE.time_interval
    ACE.liver_damage = max(0.0, ACE.liver_damage - repair)
    
    
def regen_gsh():
    if ACE.GSH_amount < ACE.GSH_baseline:
        diff_frac = (ACE.GSH_baseline - ACE.GSH_amount) / max(ACE.GSH_baseline, 1e-12)
        regen = ACE.GSH_regen_rate * diff_frac * ACE.time_interval
        ACE.GSH_amount += regen
        
        ACE.GSH_amount = min(ACE.GSH_amount, ACE.GSH_baseline)
        
def ethanol_clearance():
    if ACE.ethanol_amount <= 0:
        return
    clearance = ACE.ethanol_met_rate * ACE.time_interval
    ACE.ethanol_amount = max(0.0, ACE.ethanol_amount - clearance)
    
    
def update_hepatocyte_viability():
    ACE.hepatocyte_viability = max(0.0, 1.0 - ACE.liver_damage / max(ACE.liver_damage_threshold, 1e-12))
    
    