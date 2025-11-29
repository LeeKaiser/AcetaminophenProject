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
dose_amount = 0.150         #   amount taken per dose in [unit]

liver_volume = 1.5          #   volume of liver  in liters
liver_blood_flow = 90      #   liver blood flow in liter per hr
liver_blood_volume = 1.5    #   volume of blood in liver in liter
ace_partition_coeff = 0.669 #   partition coefficient of acetaminophen 