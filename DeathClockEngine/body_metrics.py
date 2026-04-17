import json
import os

def calculate_bmi(weight, height):

    return weight / ((height/100) **2 )

def get_bmi_modifier(bmi, gender, bmi_data):

    gender_lower = gender.lower()

    if gender_lower in ['m', 'mężczyzna']:
        gender_key = "male_hr"
    elif gender_lower in ['k', 'kobieta']:
        gender_key = "female_hr"
    else:
        raise ValueError("Niepoprawna płeć! Wpisz M lub K")

    for r in bmi_data['ranges']:
        if r['min_bmi'] <= bmi < r['max_bmi']:
            return r[gender_key]
    return 1.0



