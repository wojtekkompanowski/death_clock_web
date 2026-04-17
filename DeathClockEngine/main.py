from data_loader import load_json_data
from engine import DeathClockEngine
from occupation_choice import get_occupation_choice
from sleep_choice import get_sleep_choice
from social_relations import get_social_relations_choice
from environment_choice import get_environment_air_choice, get_environment_noise_choice
from nutrition import get_nutrition_choice, get_sugar, get_water, years_history
from genetics import get_genetics_ancestors, get_genetic_diseases
from stimulants import get_stimulants_choice, get_stimulants_dosages
from subtle_factors import get_subtle_choice


def main():


    life_table = load_json_data("life_tables.json")
    bmi_risks = load_json_data("bmi_risks.json")
    habits_risks = load_json_data("habits_risks.json")
    occupations_data = load_json_data("occupations.json")
    sleep_data = load_json_data("sleep_tables.json")
    social_data = load_json_data("social_relations.json")
    environment_data = load_json_data("environment.json")
    nutrition_data = load_json_data("nutrition.json")
    genetics_data = load_json_data("genetics.json")
    stimulants_data = load_json_data("stimulants.json")
    subtle_data = load_json_data("subtle_factors.json")


    print("=== SYSTEM PROGNOZOWANIA DŁUGOWIECZNOŚCI ===")
    print("=== Etap I ===")

    age = int(input("Podaj swój wiek: "))
    gender = input("Podaj płeć (M/K): ")
    weight = float(input("Podaj wagę (kg): "))
    height = float(input("Podaj wzrost (cm): "))

    genetics_ancestors_impact = get_genetics_ancestors(genetics_data)
    genetics_diseases_impact = get_genetic_diseases(genetics_data)

    calculator = DeathClockEngine(age, gender, life_table, weight, height)

    gen_impact = calculator.process_genetics(genetics_ancestors_impact, genetics_diseases_impact, genetics_data)

    user_bmi, impact = calculator.bmi(bmi_risks)

    print("=== Etap II ===")

    cig_per_day = 0
    cig_years = 0
    cig_active = False
    cig_quit_age = 0

    is_smoker = input("Czy kiedykolwiek paliłeś papierosy? (tak/nie): ").lower()
    if is_smoker == "tak":
        cig_per_day = int(input("Ile papierosów dziennie? "))
        cig_years = int(input("Przez ile lat paliłeś/palisz? "))
        cig_active = input("Czy palisz obecnie? (tak/nie): ").lower() == "tak"
        if not cig_active:
            cig_quit_age = int(input("W jakim wieku rzuciłeś? "))
        else:
            cig_quit_age = age  # Jeśli pali nadal, wiek rzucenia to obecny wiek

    # --- LOGIKA DLA VAPE ---
    vape_years = 0
    vape_active = False
    vape_quit_age = 0

    is_vaper = input("Czy kiedykolwiek używałeś e-papierosów? (tak/nie): ").lower()
    if is_vaper == "tak":
        vape_years = int(input("Przez ile lat używałeś/używasz e-peta? "))
        vape_active = input("Czy vapujesz obecnie? (tak/nie): ").lower() == "tak"
        if not vape_active:
            vape_quit_age = int(input("W jakim wieku rzuciłeś? "))
        else:
            vape_quit_age = age

    # --- LOGIKA DLA PODGRZEWACZY ---

    heat_years = 0
    heat_active = False
    heat_quit_age = 0
    stick_per_day = 0

    is_heat = input("Czy kiedykolwiek używałeś podgrzewaczy tytoniu? (tak/nie): ").lower()
    if is_heat == "tak":
        stick_per_day = int(input("Ile wkładów dziennie? "))
        heat_years = int(input("Przez ile lat używałeś/używasz podgrzewaczy tytoniu? "))
        heat_active = input("Czy używasz podgrzewaczy tytoniu obecnie? (tak/nie): ").lower() == "tak"
        if not heat_active:
            heat_quit_age = int(input("W jakim wieku rzuciłeś? "))
        else:
            heat_quit_age = age


    nicotine_impact = calculator.process_nicotine(cig_years, cig_per_day, cig_active, cig_quit_age, vape_years, vape_active, vape_quit_age,
        habits_risks, stick_per_day, heat_years, heat_active, heat_quit_age)


    # --- LOGIKA DLA ALKOHOLU ---

    beer_quantity = 0
    wine_quantity = 0
    vodka_quantity = 0
    alcohol_50 = 0
    alcohol_75 = 0
    binge_drinking = False

    is_alcohol_drinker = input("Czy jesteś abstynentem? (tak/nie): ").lower()
    if is_alcohol_drinker == "nie":
        beer_quantity = int(input("Ile pijesz piwa tygodniowo? (1 porcja/puszka = 500 ml): "))
        wine_quantity = int(input("Ile pijesz wina tygodniowo? (1 porcja/lampka = 175 ml): "))
        vodka_quantity = int(input("Ile pijesz alkoholu 40% tygodniowo? (1 porcja/kieliszek = 50 ml): "))
        alcohol_50 = int(input("Ile pijesz alkoholu od 41% do 50% (1 porcja/kieliszek = 50 ml): "))
        alcohol_75 = int(input("Ile pijesz alkoholu od 51% do 70% (1 porcja/kieliszek = 50 ml): "))
        binge_drinking = input("Czy pijesz gwałtownie? Ostra najebka w jedną noc (tak/nie): ")
        if binge_drinking == "tak":
            binge_drinking = True
        else:
            binge_drinking = False

    alcohol_impact = calculator.process_alcohol(beer_quantity, wine_quantity, vodka_quantity, alcohol_50, alcohol_75, habits_risks, gender, binge_drinking)

    # --- LOGIKA DLA AKTYWNOŚCI ---

    years_activty = int(input("Ile lat w swoim życiu regularnie uprawiałeś sport? "))

    print("Wybierz swój obecny poziom aktywności:")
    print("1. Siedzący (brak ruchu, praca biurowa) [Sedentary]")
    print("2. Aktywny (spacerujesz, trenujesz 2-3x w tyg.) [Active]")
    print("3. Sportowiec (regularne, ciężkie treningi) [Athlete]")

    levels = {
        "1": "sedentary",
        "2": "active",
        "3": "athlete"
    }

    choice = input("Twój wybór: ")
    current_lvl = levels.get(choice, "sedentary")

    activity_impact = calculator.process_activity(years_activty, habits_risks, current_lvl)

    print("=== Etap III ===")

    occ_key = get_occupation_choice(occupations_data)
    job_info = occupations_data['occupations'][occ_key]

    print(f"\nWybrany zawód: {job_info['name']}")
    print("Jak oceniasz swój poziom stresu na tle innych osób w tej branży?")
    print("1. Mniejszy (spokojna posada, dobre relacje)")
    print("2. Typowy (standard dla tego zawodu)")
    print("3. Znacznie większy (ogromna presja, mobbing, nadgodziny)")

    stress_choice = input("Wybierz (1/2/3): ")
    stress_map = {"1": -0.05, "2": 0.0, "3": 0.10}
    stress_mod = stress_map.get(stress_choice, 0.0)

    occ_impact = calculator.process_occupation(occ_key, stress_mod, occupations_data)

    print("=== Etap IV ===")

    # --- LOGIKA DLA SNU ---

    sleep_key = get_sleep_choice(sleep_data)

    sleep_impact = calculator.process_sleep(sleep_key, sleep_data)

    # --- LOGIKA DLA RELACJI SPOŁECZNYCH ---

    relation_key = get_social_relations_choice(social_data)

    relation_impact = calculator.process_relation(relation_key, social_data)

    # --- LOGIKA DLA ŚRODOWISKA ---

    years_in_smog = int(input("Ile lat spędziłeś w miejscach o złym powietrzu? "))

    environment_air_key = get_environment_air_choice(environment_data)

    environment_noise_key = get_environment_noise_choice(environment_data)

    environment_impact = calculator.process_environment(years_in_smog, environment_air_key, environment_noise_key, environment_data)

    # --- LOGIKA DLA ŻYWIENIA ---

    nutrition_diet_choice = get_nutrition_choice(nutrition_data)
    nutrition_years_penalty = years_history(nutrition_data)
    nutrition_sugar = get_sugar()
    nutrition_water = get_water()

    nutrition_impact = calculator.process_nutrition(nutrition_diet_choice, nutrition_years_penalty, nutrition_water, nutrition_sugar, nutrition_data)

    # --- LOGIKA DLA KOFEINY ---
    stimulants_choice = get_stimulants_choice(stimulants_data)
    stimulants_dosages = get_stimulants_dosages(stimulants_data)
    stimulants_impact = calculator.process_stimulants(stimulants_choice, stimulants_dosages, stimulants_data)

    # --- LOGIKA DLA CZYNNIKÓW UKRYTYCH ---
    subtle_factors_choices = get_subtle_choice(subtle_data)
    subtle_factors_impact = calculator.process_subtle_factors(subtle_factors_choices, subtle_data)

    final_age = calculator.calculate_results()
    risk_penalty = calculator.process_statistical_risk(final_age)
    final_age += risk_penalty

    print("-" * 30)
    print(f"\n[INFO] Twoja baza życia została skorygowana o {gen_impact} lat ze względów genetycznych.")
    print(f"Bazowy pozostały czas życia (po genetyce): {calculator.base_years:.1f} lat.")
    print(f"Twoje BMI wynosi: {user_bmi:.1f}")
    print("-" * 30)

    # --- UŻYWKI ---
    if nicotine_impact != 0:
        print(f"Łączny wpływ nikotyny: {nicotine_impact} lat.")
    else:
        print("Brak obciążeń nikotynowych.")

    if alcohol_impact != 0:
        print(f"Łączny wpływ alkoholu: {alcohol_impact} lat.")
    else:
        print("Brak obciążeń alkoholowych.")

    # --- STYL ŻYCIA ---
    if activity_impact > 0:
        print(f"Aktywność fizyczna: +{activity_impact} lat.")
    else:
        print(f"Brak ruchu: {activity_impact} lat.")

    if sleep_impact != 0:
        print(f"Wpływ jakości snu: {sleep_impact} lat.")

    print(f"Wpływ relacji społecznych: {relation_impact} lat.")

    # --- PRACA I ŚRODOWISKO ---
    if occ_impact != 0:
        print(f"Wpływ zawodu i stresu: {occ_impact} lat.")

    print(f"Wpływ środowiska (smog/hałas): {environment_impact} lat.")

    # --- NOWOŚĆ: ŻYWIENIE I METABOLIZM ---
    # Tutaj zakładamy, że nutrition_impact to wynik z metody process_nutrition
    print(f"Wpływ nawyków żywieniowych: {nutrition_impact} lat.")
    if nutrition_sugar > 0:  # Jeśli hr_extra było wybrane
        print(f"  -> W tym kara za nadmiar cukru.")
    if nutrition_water < 0:
        print(f"  -> W tym kara za słabe nawodnienie.")

    # --- NOWOŚĆ: KOFEINA I STYMULANTY ---
    if stimulants_impact > 0:
        print(f"Wpływ kofeiny (antyoksydanty): +{stimulants_impact} lat.")
    elif stimulants_impact < 0:
        print(f"Wpływ kofeiny (nadmiar/energetyki): {stimulants_impact} lat.")
    else:
        print("Kofeina nie wpływa na Twój wynik.")
    if subtle_factors_impact > 0:
        print(f"Wpływ czynników ukrytych: {subtle_factors_impact}")
    else:
        print(f"Czynniki ukryte nie wpływają na długość twojego życia.")
    print(f"Statystyczna korekta ryzyka losowego: -{risk_penalty} lat.")
    print("*(Uwzględnia statystyczne prawdopodobieństwo wypadków oraz wzrastającą z wiekiem podatność na urazy)*")

    print("-" * 30)
    print(f"PRZEWIDYWANY WIEK DOŻYCIA: {final_age} lat.")
    print("-" * 30)

main()