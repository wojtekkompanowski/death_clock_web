

def calculate_smoking_impact(cigarette_per_day, years_of_smoking, habits_risks, active_smoker, quit_age):
    cigarette_per_year = (cigarette_per_day / 20) * years_of_smoking

    hr = 1.0 + (cigarette_per_year * habits_risks['smoking']['hr_per_pack_year'])


    if not active_smoker:
        if quit_age < 30:
            hr = 1.0 + (hr - 1.0) * (1- habits_risks['smoking']['recovery_bonus_before_30'])
        else:
            hr = 1.0 + (hr - 1.0) * habits_risks['smoking']['recovery_factor_after_quitting']

    hr = min(hr, habits_risks['smoking']['max_hr'])

    return hr

def calculate_heat_not_burn(stick_per_day, years_of_smoking, habits_risks, active_smoker, quit_age):

    hr = 1.0 + (stick_per_day * habits_risks['heat_not_burn']['hr_per_stick_year'])

    if not active_smoker:
        if quit_age < 30:
            hr = 1.0 + (hr - 1.0) * (1- habits_risks['heat_not_burn']['recovery_bonus_before_30'])
        else:
            hr = 1.0 + (hr - 1.0) * habits_risks['heat_not_burn']['recovery_factor_after_quitting']

    hr = min(hr, habits_risks['heat_not_burn']['max_hr'])

    return hr

def calculate_e_cigarettes_smoking_impact(years_of_smoking, habits_risks, active_smoker, quit_age):

    hr = 1.0 + (years_of_smoking * habits_risks['e_cigarettes']['hr_per_vape_year'])

    if not active_smoker:
        if quit_age < 30:
            hr = 1.0 + (hr - 1.0) * (1 - habits_risks['e_cigarettes']['recovery_bonus_before_30'])
        else:
            hr = 1.0 + (hr - 1.0) * habits_risks['e_cigarettes']['recovery_factor_after_quitting']


    hr = min(hr, habits_risks['e_cigarettes']['max_hr'])

    return hr

def calculate_alcohol_impact(beer_quantity, wine_quantity, vodka_quantity, alcohol_50_quantity, alcohol_75_quantity, habits_risks, gender, binge_drinking):

    beer = 2
    wine = 2
    vodka = 1.6
    alcohol_50 = 1.9
    alcohol_75 = 2.6

    total_units = (beer * beer_quantity) + (wine * wine_quantity) + (vodka * vodka_quantity) + (alcohol_50 * alcohol_50_quantity) + (alcohol_75 * alcohol_75_quantity)

    if gender.lower() in ['m', 'mężczyzna', 'mezczyzna']:
        gender_key = habits_risks['alcohol']['units_limit_male']
    else:
        gender_key = habits_risks['alcohol']['units_limit_female']

    surplus = max(0, total_units - gender_key)

    hr = 1.0 + (surplus * habits_risks['alcohol']['hr_per_excess_unit'])

    if binge_drinking:
        hr += habits_risks['alcohol']['binge_penalty']

    hr = min(hr, habits_risks['alcohol']['max_hr'])

    return hr

def physical_activity(year_activity, habits_risks):

    bonus = year_activity * habits_risks['physical_activity']['bonus_per_year_active']

    bonus = min(bonus, habits_risks['physical_activity']['max_bonus_years'])

    return bonus
