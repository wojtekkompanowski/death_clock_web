
from .body_metrics import calculate_bmi,  get_bmi_modifier
from .habits import calculate_smoking_impact, calculate_e_cigarettes_smoking_impact, calculate_heat_not_burn, calculate_alcohol_impact, physical_activity

class DeathClockEngine:
    def __init__(self, age, gender, life_table, weight, height):
        self.age = age
        self.gender = gender
        self.base_years = self.get_base_expectancy(life_table) #średnia z bazy ile lat pozostało
        self.adjustments = [] # mnożnik pozostałych lat

        #potrzebne do liczenia hr przy paleniu
        self.hr_smoking = None
        self.hr_e_smoking = None

        #potrzebne do bmi
        self.weight = weight
        self.height = height

    def process_genetics(self, ancestors_key, diseases_key, genetics_data):

        gen_section = genetics_data['genetics_data']

        ancestors_impact = gen_section['ancestors_longevity'][ancestors_key]['impact_years']
        diseases_impact = gen_section['hereditary_risks'][diseases_key]['impact_years']

        total_genetics_impact = ancestors_impact + diseases_impact

        self.base_years += total_genetics_impact

        return total_genetics_impact

    def add_modifier(self, value):
        self.adjustments.append(value) # dodawanie kolejnych mnożników


    def get_base_expectancy(self, life_table):

        # sprawdzanie jakiej płci jest użytkownik
        if self.gender.lower() in ['m', 'mężczyzna', 'mezczyzna']:
            gender_key = "male"
        else:
            gender_key = "female"


        #wybieramy z tabeli tylko płeć wpisaną
        life_tables = life_table[gender_key]

        #Wypisujemy wszystkie lata jednej płci
        all_ages = []

        for k in life_tables.keys():
            all_ages.append(int(k))

        #wypisujemy największy wiek czyli 100
        max_age = max(all_ages)

        #sprawdzamy czy wiek podany jest większy od 100, jeśli tak to przypisujemy 100, jeśli nie zostawiamy jaki podał użytkownik
        if self.age > max_age:
            search_age = max_age
        else:
            search_age = self.age

        search_age = str(search_age)

        value = life_tables[search_age]

        return float(value)

    def calculate_results(self):

        #przypisujemy bazowe pozostałe lata życia
        current_remaining = self.base_years

        #dodajemy
        for m in self.adjustments:
            current_remaining += m

        #zaokrąglamy
        return round(self.age + current_remaining, 2)

    def bmi(self, bmi_data):

        #liczmy bmi z funkcji calculate_bmi z pliku body_metrics.py
        bmi = calculate_bmi(self.weight, self.height)

        #wyciągamy z bazy modyfikator używając get_bmi_modifier z pliku body_metrics.py
        hr = get_bmi_modifier(bmi, self.gender, bmi_data)

        #liczymy ile bmi nam doda lub zabierze lat (pozostałe lata podzielić na modyfikator np 54.5 / 1.25 (otyłość) zotaje nam 43,6)
        adjusted_remaining = float(self.base_years) / hr

        #liczymy różnicę między bazową pozostałością naszych lat a latami po modyfikatorzę czyli 43,6 - 54.5, co dstaje -10.9, to kara za otyłość
        impact = adjusted_remaining - float(self.base_years)

        self.adjustments.append(impact)

        return round(bmi, 2), round(impact, 2)


    def process_nicotine(self, cig_years, cig_per_day, cig_active, cig_quit_age,
                         vape_years, vape_active, vape_quit_age, habits_risks,
                         stick_per_day, heat_years, heat_active, heat_quit_age):

        # 1. Obliczamy cząstkowe HR (korzystając z Twoich funkcji pomocniczych)
        hr_smoke = calculate_smoking_impact(cig_per_day, cig_years, habits_risks, cig_active, cig_quit_age)
        hr_vape = calculate_e_cigarettes_smoking_impact(vape_years, habits_risks, vape_active, vape_quit_age)
        hr_heat = calculate_heat_not_burn(stick_per_day, heat_years, habits_risks, heat_active, heat_quit_age)

        # 2. Łączymy ryzyka (1.0 + nadwyżka z papierosów + nadwyżka z vape)
        total_hr = 1.0 + (hr_smoke - 1.0) + (hr_vape - 1.0) + (hr_heat - 1.0)

        # 3. Sprawdzamy Dual Use (czy kiedykolwiek używał obu)
        if cig_years > 0 and vape_years > 0:
            total_hr += habits_risks['dual_use']['extra_hr_penalty']
        elif cig_years > 0 and heat_years > 0:
            total_hr += habits_risks['dual_use']['extra_hr_penalty']
        elif vape_years > 0 and heat_years > 0:
            total_hr += habits_risks['dual_use']['extra_hr_penalty']

        # 4. Finalne przeliczenie na lata (TYLKO TUTAJ)
        impact = (float(self.base_years) / total_hr) - float(self.base_years)

        # 5. Dodajemy do listy tylko ten jeden, wspólny wynik
        self.adjustments.append(impact)

        return round(impact, 2)

    def process_alcohol(self, beer_quantity, wine_quantity, vodka_quantity, alcohol_50_quantity, alcohol_75_quantity, habits_risks, gender, binge_drinking):

        hr = calculate_alcohol_impact(beer_quantity, wine_quantity, vodka_quantity, alcohol_50_quantity, alcohol_75_quantity, habits_risks, gender, binge_drinking)

        impact = (float(self.base_years) / hr) - float(self.base_years)

        self.adjustments.append(impact)

        return round(impact, 2)

    def process_activity(self, year_activity, habits_risks, current_level):

        bonus = physical_activity(year_activity, habits_risks)

        activity_hr = habits_risks['physical_activity']['current_activity_modifiers'].get(current_level, 1.0)

        current_impact = (float(self.base_years) / activity_hr) - float(self.base_years)

        total_impact = bonus + current_impact

        self.adjustments.append(total_impact)

        return round(total_impact, 2)

    def process_occupation(self, occ_key, stress_modifier, occupations_data):

        job = occupations_data['occupations'][occ_key]

        base_hr = job['stress_hr']
        hazard_hr = job['environment_hazard']

        final_job_hr = base_hr + stress_modifier

        total_occ_hr = final_job_hr + (hazard_hr - 1.0)

        impact = (float(self.base_years) / total_occ_hr) - float(self.base_years)

        self.adjustments.append(impact)

        return round(impact, 2)


    def process_sleep(self, sleep_key, sleep_data):

        hr = sleep_data['sleep_health'][sleep_key]['hr']

        impact = (float(self.base_years) / hr) - float(self.base_years)

        self.adjustments.append(impact)

        return round(impact, 2)

    def process_relation(self, relation_keys, social_data):

        hr = social_data['social_relations'][relation_keys]['hr']

        impact = (float(self.base_years) / hr) - self.base_years

        self.adjustments.append(impact)

        return round(impact, 2)

    def process_environment(self, years_in_smog, environment_air_key, environment_noise_key, environment_data):

        penalty_smog = years_in_smog * environment_data['environment_data']['history']['penalty_per_year_polluted']

        penalty_smog = min(penalty_smog, environment_data['environment_data']['history']['max_history_penalty_years'])

        air_hr = environment_data['environment_data']['current_air'][environment_air_key]['hr']

        noise_hr = environment_data['environment_data']['current_noise'][environment_noise_key]['hr']

        hr = air_hr * noise_hr

        impact = float(self.base_years / hr) - self.base_years

        total_impact = impact - penalty_smog

        self.adjustments.append(total_impact)

        return round(total_impact, 2)

    def process_nutrition(self, data, nutrition_db):
        # 1. Pobieramy bazowy HR diety
        diet_key = data['diet_choice']
        diet_hr = nutrition_db['nutrition_data']['diet_patterns'][diet_key]['hr']

        # 2. Cukier i Woda (Mapujemy wybór z frontendu na wartości z bazy)
        # Zakładamy, że frontend wysyła 'sugar_addiction': true/false
        sugar_hr = 0.10 if data.get('sugar_addiction') else 0.0

        # 3. Obliczamy wpływ na podstawie HR (Ryzyko metaboliczne)
        total_hr = diet_hr + sugar_hr
        impact = (self.base_years / total_hr) - self.base_years

        # 4. Kara za historię (Logika dekadowa)
        years_bad = data.get('years_history_input', 0)
        history_cfg = nutrition_db['nutrition_data']['history']
        history_penalty = (years_bad / 10) * history_cfg['poor_nutrition_decade_penalty']
        history_penalty = min(history_penalty, history_cfg['max_history_penalty'])

        # 5. Woda (Stały wpływ lat)
        water_impact = -1.5 if data.get('low_hydration') else 0.0

        total_nutrition_impact = impact - history_penalty + water_impact
        self.adjustments.append(total_nutrition_impact)
        return round(total_nutrition_impact, 2)

    def process_stimulants(self, data, caffeine_db):
        # Pobieramy dane z bazy
        source = data['stimulants_choice']  # np. 'energy_only'
        dosage = data['stimulants_dosages']  # np. 'high'

        caffeine_cfg = caffeine_db['caffeine_data']

        hr_mod = caffeine_cfg['sources'][source]['hr_modifier']
        multiplier = caffeine_cfg['dosages'][dosage]['multiplier']

        # Wzór: total_hr = 1.0 + (modyfikator * dawka)
        total_hr = 1.0 + (hr_mod * multiplier)

        impact = (self.base_years / total_hr) - self.base_years

        self.adjustments.append(impact)
        return round(impact, 2)

    def process_statistical_risk(self, predicted_age):

        # Statystycznie to ok. 1% szansy na skrócenie życia o połowę,
        base_risk = 0.7

        fragility_penalty = 0
        if predicted_age > 75:
            fragility_penalty = (predicted_age - 75) * 0.12

        total_risk_deduction = base_risk + fragility_penalty

        return round(total_risk_deduction, 2)

    def process_subtle_factors(self, choices, subtle_data):
        total_impact = 0

        # Wyciągamy właściwy słownik z pliku
        data_dict = subtle_data.get('subtle_data', {})

        # Iterujemy po liście kluczy przekazanej z GUI
        for key in choices:
            if key in data_dict:
                total_impact += data_dict[key]['impact']

        return total_impact
