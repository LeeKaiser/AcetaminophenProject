#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:24:33 2025

@author: kaiserlee
"""

#global variables stored here to avoid circular import
fig_title_prefix = 'sulf_50'
fig_dir = 'analysis_8'
save_plt = True

time = 24                    #   amount of time in simulation in hours
time_interval = 0.01         #   amount of time passed per interval (total time steps = time/time_interval)

dose_interval = 4           #   amount of time between dose
dose_count = 1              #   amount of dose taken
dose_amount = 650           #   amount taken per dose in mg

isFed = False               #   whether the individual has fasted or has eaten
absorb_constant = 2 / 60.0       #absorption constant of ace

liver_volume = 1.5          #   volume of liver  in liters
liver_blood_flow = 90      #   liver blood flow in liter per hr
liver_blood_volume = 1.5    #   volume of blood in liver in liter
ace_partition_coeff = 0.669 #   partition coefficient of acetaminophen 

glu_max_met_rate = 146.63       #   glucuronidation max metabolic rate in mg/hr
glu_drug_con = 1041.5          #   glucuronidation drug concentration in mg/L
sulf_max_met_rate = 3 * 0.5      #   sulfation max metabolic rate in mg/hr
sulf_drug_con = 14.7          #   sulfation drug concentration in mg/L
p450_max_met_rate = 8.0     #   p450 max metabolic rate in mg/hr
p450_drug_con = 120         #   p450 enzyme concentration in mg/L


GSH_baseline = 8.0          #   base amount of glutathione, mmol
GSH_amount = 8.0            #   live pool
GSH_min_threshold = 0.3     #   30% required for normal detox
GSH_km = 1.0                #   mmol, used for detox calc
NAPQI_detox_max_rate = 12.0 #   mmol/hr

GSH_regen_rate = 0.8        #   mmol/hr, towards baseline

ethanol_amount = 0        #   current ethanol in sys, 0 is sober (mmol)
ethanol_met_rate = 7.0      #   mmol/hr
ethanol_induction_factor = 2.0  #   max induction value
ethanol_induction_k = 10.0  #   amount of ethanol at which half induction occurs
ethanol_GSH_compete = 0.6   #   mmol/hr tied up by ethanol metabolism

NAPQI_toxic_threshold = 0.05#   mg/L; below this damage is negligible
damage_exponent = 2.0       #   exponent to make damage rise steeply above threshold
toxicity_constant = 0.005   #   baseline damage scale (damage units per hour per normalized excess)

liver_repair_rate = 0.02    #   damage units repaired per hour
liver_damage = 0.0          #   cumulative damage 
liver_damage_threshold = 8.0#   damage at which hepatocyte viability becomes 0

hepatocyte_viability = 1.0  #   1 = fully viable, 0 = lost

min_damage_increment = 1e-8