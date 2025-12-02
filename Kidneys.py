# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 16:30:20 2025

@author: Vivian
"""
import ace_global_vars as ACE
import Blood_Stream as BS


#BELOW DEFAULT CAN BE OVERRIDDEN BY ADDING TO ACE_GLOBAL_VARS
# Glomerular filtration rate (mL / min)
GFR_ML_MIN = getattr(ACE, "kidney_GFR_ml_min", 120.0)
BLOOD_VOLUME_L = getattr(ACE, "blood_volume", 5.0)

# Per-metabolite reabsorption fractions (fraction of filtered amount reabsorbed back to blood)
DEFAULT_REABS_FRAC = getattr(ACE, "kidney_default_reabs_frac", 0.0)
REABS_FRAC_MAP = getattr(ACE, "kidney_reabsorption_frac", {
    "ace": DEFAULT_REABS_FRAC,
    "ace_glu": DEFAULT_REABS_FRAC,
    "ace_sulf": DEFAULT_REABS_FRAC,
    "NAPQI_glu": DEFAULT_REABS_FRAC
})

urine_volume_ml = 0.0
urine_ace = 0.0
urine_ace_glu = 0.0
urine_ace_sulf = 0.0
urine_NAPQI_glu = 0.0
urine_volume_list = []
urine_ace_list = []
urine_ace_glu_list = []
urine_ace_sulf_list = []
urine_NAPQI_glu_list = []

def _concentration_from_amount(amount_mg, volume_l):
    if volume_l <= 0:
        return 0.0
    return amount_mg / volume_l

def _filter_amount(conc_mg_per_L, gfr_ml_min, time_minutes):
    volume_cleared_L = (gfr_ml_min / 1000.0) * time_minutes
    return conc_mg_per_L * volume_cleared_L

def step(time_minutes=1.0):
    global urine_volume_ml, urine_ace, urine_ace_glu, urine_ace_sulf, urine_NAPQI_glu

    ace = getattr(BS, "ace_in_sys", 0.0)
    ace_glu = getattr(BS, "ace_glu_in_sys", 0.0)
    ace_sulf = getattr(BS, "ace_sulf_in_sys", 0.0)
    napqi_glu = getattr(BS, "NAPQI_glu_in_sys", 0.0)
    
    C_ace = _concentration_from_amount(ace, BLOOD_VOLUME_L)
    C_ace_glu = _concentration_from_amount(ace_glu, BLOOD_VOLUME_L)
    C_ace_sulf = _concentration_from_amount(ace_sulf, BLOOD_VOLUME_L)
    C_napqi_glu = _concentration_from_amount(napqi_glu, BLOOD_VOLUME_L)

    filt_ace = _filter_amount(C_ace, GFR_ML_MIN, time_minutes)
    filt_ace_glu = _filter_amount(C_ace_glu, GFR_ML_MIN, time_minutes)
    filt_ace_sulf = _filter_amount(C_ace_sulf, GFR_ML_MIN, time_minutes)
    filt_napqi_glu = _filter_amount(C_napqi_glu, GFR_ML_MIN, time_minutes)
    
    reabs_ace = REABS_FRAC_MAP.get("ace", DEFAULT_REABS_FRAC) * filt_ace
    reabs_ace_glu = REABS_FRAC_MAP.get("ace_glu", DEFAULT_REABS_FRAC) * filt_ace_glu
    reabs_ace_sulf = REABS_FRAC_MAP.get("ace_sulf", DEFAULT_REABS_FRAC) * filt_ace_sulf
    reabs_napqi_glu = REABS_FRAC_MAP.get("NAPQI_glu", DEFAULT_REABS_FRAC) * filt_napqi_glu

    excr_ace = max(0.0, filt_ace - reabs_ace)
    excr_ace_glu = max(0.0, filt_ace_glu - reabs_ace_glu)
    excr_ace_sulf = max(0.0, filt_ace_sulf - reabs_ace_sulf)
    excr_napqi_glu = max(0.0, filt_napqi_glu - reabs_napqi_glu)

    BS.ace_in_sys = max(0.0, ace - excr_ace)
    BS.ace_glu_in_sys = max(0.0, ace_glu - excr_ace_glu)
    BS.ace_sulf_in_sys = max(0.0, ace_sulf - excr_ace_sulf)
    BS.NAPQI_glu_in_sys = max(0.0, napqi_glu - excr_napqi_glu)

    urine_added_ml = (GFR_ML_MIN * time_minutes)  #plasma filtered volume; not realistic urine but useful bookkeeping
    urine_volume_ml += urine_added_ml
    
    urine_ace += excr_ace
    urine_ace_glu += excr_ace_glu
    urine_ace_sulf += excr_ace_sulf
    urine_NAPQI_glu += excr_napqi_glu

    urine_volume_list.append(urine_added_ml)
    urine_ace_list.append(excr_ace)
    urine_ace_glu_list.append(excr_ace_glu)
    urine_ace_sulf_list.append(excr_ace_sulf)
    urine_NAPQI_glu_list.append(excr_napqi_glu)

    return {
        "urine_volume_ml": urine_added_ml,
        "ace_mg": excr_ace,
        "ace_glu_mg": excr_ace_glu,
        "ace_sulf_mg": excr_ace_sulf,
        "NAPQI_glu_mg": excr_napqi_glu
    }

