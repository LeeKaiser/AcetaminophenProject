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

def step():
    print("liver metabolizes acetaminophen to ace_glu, ace_sulf, and NAPQI")
    
    print("then NAPQI is detoxified to NAPQI_glu")