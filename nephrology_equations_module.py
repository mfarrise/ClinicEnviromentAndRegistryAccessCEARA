"""this module will hold the classes and functions related to nephrology"""

"""
This module holds nephrology-related calculations
(eGFR CKD-EPI 2021, race-free)
"""


def calculate_eGFR(age=45.0, cr=1.0, gender="male", unit="mg/dl"):
    """
    CKD-EPI 2021 race-free eGFR equation


    Parameters
    ----------
    age : float
    Age in years
    cr : float
    Serum creatinine
    gender : str
    'male' or 'female'
    unit : str
    'mg/dl' or 'umol/l'


    Returns
    -------
    egfr : float
    eGFR in ml/min/1.73m²
    """


    # Normalize inputs
    gender = gender.strip().lower()
    unit = unit.strip().lower()


    # Convert creatinine if needed
    if unit in ["umol/l", "µmol/l"]:
        cr = cr / 88.4 # µmol/L → mg/dL


    # Sex-specific constants (CKD-EPI 2021)
    if gender == "female":
        k = 0.7
        a = -0.241
        sex_factor = 1.012
    elif gender == "male":
        k = 0.9
        a = -0.302
        sex_factor = 1.0
    else:
        raise ValueError("gender must be 'male' or 'female'")


    egfr = (
        142
        * (min(cr / k, 1) ** a)
        * (max(cr / k, 1) ** -1.200)
        * (0.9938 ** age)
        * sex_factor
        )


    return egfr

def contrast_risk(egfr=120,age=30,contrast=100,hf='n',baloon='n',hypo_tension='n',dm='n',anemia='n'):

        score=0.0
        risk=0.0
        dialysis=0.0
        #1
        if hypo_tension.lower() == "y":
            score +=5
        #2
        if baloon.lower() == "y":
            score +=5
        #3
        if hf.lower() == "y":
            score +=5
        #4
        if age>75:
            score +=4
        #5
        if anemia.lower() == "y":
            score +=3
        #6
        if dm.lower() == "y":
            score +=3
        #7
        score +=(contrast//100)
        #8
        if egfr<20:
            score +=6
        elif egfr<40:
            score +=4
        elif egfr<60:
            score +=2
        # final verdict
        if score <= 5 :
            #print("risk of CIN 7.5% and risk of dialysis 0.04%")
            risk=7.5
            dialysis=0.04
        elif score >= 6 and score <= 10 :
            #print("risk of CIN 14% and risk of dialysis 0.12%")
            risk=14
            dialysis=0.12
        elif score >= 11 and score <= 15 :
            #print("risk of CIN 26.1% and risk of dialysis 1.09%")
            risk=26.1
            dialysis=1.09
        elif score >= 16 :
            #print("risk of CIN 57.3% and risk of dialysis 12.6%")
            risk=57.3
            dialysis=12.6
        return score,risk,dialysis










