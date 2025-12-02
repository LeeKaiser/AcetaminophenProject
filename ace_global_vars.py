#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:24:33 2025

@author: kaiserlee
"""

#global variables stored here to avoid circular import
time = 30                    #   amount of time in simulation
time_interval = 0.01         #   amount of time passed per interval (total time steps = time/time_interval)

dose_interval = 8           #   amount of time between dose
dose_count = 3              #   amount of dose taken
dose_amount = 1000           #   amount taken per dose in mg


liver_volume = 1.5          #   volume of liver  in liters
liver_blood_flow = 90      #   liver blood flow in liter per hr
liver_blood_volume = 1.5    #   volume of blood in liver in liter
ace_partition_coeff = 0.669 #   partition coefficient of acetaminophen 

glu_max_met_rate = 146.63      #   glucuronidation max metabolic rate in mg/hr
glu_drug_con = 1041.5          #   glucuronidation drug concentration in mg/L
sulf_max_met_rate = 3      #   sulfation max metabolic rate in mg/hr
sulf_drug_con = 14.7          #   sulfation drug concentration in mg/L
p450_max_met_rate = 8.0     #   p450 max metabolic rate in mg/hr
p450_drug_con = 120         #   p450 enzyme concentration in mg/L


GSH_baseline = 8.0          #   base amount of glutathione, mmol
GSH_amount = 8.0            #   live pool
GSH_min_threshold = 0.3     #   30% required for normal detox
GSH_km = 1.0                #   mmol, used for detox calc
NAPQI_detox_max_rate = 12.0 #   mmol/hr

GSH_regen_rate = 0.8        #   mmol/hr, towards baseline

ethanol_amount = 0.0        #   current ethanol in sys, 0 is sober
ethanol_met_rate = 7.0      #   mmol/hr
ethanol_induction_factor = 2.0  #   max induction value
ethanol_induction_k = 10.0  #   amount of ethanol at which half induction occurs
ethanol_GSH_compete = 0.6   #   mmol/hr tied up by ethanol metabolism

liver_damage = 0.0          #   cummulative damage, arbitrary unit (bad i know)
liver_damage_threshold = 8.0#   damage at which viability is 0
toxicity_constant = 0.06    #   scales unmetabolized NAPQI to liver damage over time

hepatocyte_viability = 1.0  #   1 = fully viable, 0 = lost