#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:24:33 2025

@author: kaiserlee
"""

#global variables stored here to avoid circular import
time = 5                    #   amount of time in simulation
time_interval = 0.1         #   amount of time passed per interval (total time steps = time/time_interval)

dose_interval = 1           #   amount of time between dose
dose_count = 3              #   amount of dose taken
dose_amount = 150           #   amount taken per dose in mg


liver_volume = 1.5          #   volume of liver  in liters
liver_blood_flow = 90      #   liver blood flow in liter per hr
liver_blood_volume = 1.5    #   volume of blood in liver in liter
ace_partition_coeff = 0.669 #   partition coefficient of acetaminophen 

glu_max_met_rate = 145      #   glucuronidation max metabolic rate in mg/hr
glu_drug_con = 220          #   glucuronidation drug concentration in mg/L
sulf_max_met_rate = 65      #   sulfation max metabolic rate in mg/hr
sulf_drug_con = 20          #   sulfation drug concentration in mg/L
p450_max_met_rate = 8.0     #   p450 max metabolic rate in mg/hr
p450_drug_con = 120         #   p450 enzyme concentration in mg/L


GSH_baseline = 8.0          #   base amount of glutathione, mmol
GSH_amount = 8.0            #   live pool
GSH_min_threshold = 0.3     #   30% required for normal detox
GSH_km = 1.0                #   mmol, used for detox calc
NAPQI_detox_max_rate = 12.0 #   mmol/hr