#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 18:14:42 2025

@author: kaiserlee
"""

#represents digestive system
import ace_global_vars as ACE
import numpy as np

isFed = False
aceInStomach = 0
aceInIntestine = 0
lastDose = 0

def step():
    
    stomachStep()
    intestineStep()
    
    print("step in digestive system done")
    

def stomachStep():
    print("step in stomach done")
    
def intestineStep():
    print("step in intestine done")