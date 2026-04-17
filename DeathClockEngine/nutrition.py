def get_nutrition_choice(nutrition_data):

    nutrition_section = nutrition_data['nutrition_data']

    nutrition_key = nutrition_section['diet_patterns']

    nutrition_key_list = list(nutrition_key.keys())

    print("\n--- WYBÓR NAWYKÓW ŻYWIENIA ---")
    for i, val in enumerate(nutrition_key.values(), start=1):
        print(f"{i}. {val['name']}")


    choice = int(input("Wybierz najbardziej zbliżoną dietę do swojej: ")) - 1
    choice_key = nutrition_key_list[choice]

    return choice_key

def get_sugar():

    sugar_mapping = {
        1: 0.0,  # Okazjonalnie
        2: 0.04,  # Umiarkowanie
        3: 0.10  # Często
    }

    print("\n--- SPOŻYCIE CUKRU I SŁODZONYCH NAPOJÓW ---")
    print("Jak często w Twojej diecie pojawiają się słodycze, desery,")
    print("napoje gazowane, energetyki lub słodzenie kawy/herbaty?")
    print("1. Okazjonalnie (rzadziej niż raz w tygodniu)")
    print("2. Umiarkowanie (2-4 razy w tygodniu)")
    print("3. Często (codziennie lub kilka razy dziennie)")

    user_choice_sugar = int(input("\nWybierz poziom spożycia (1-3): "))

    hr_extra = sugar_mapping.get(user_choice_sugar, 0.0)

    return hr_extra

def get_water():

    water_mapping = {
        1: -1.5,  # Poniżej 1L
        2: 0.0,  # 1-2L
        3: 0.5  # Powyżej 2L
    }

    print("\n--- NAWODNIENIE ORGANIZMU ---")
    print("Ile czystej wody (lub niesłodzonych naparów ziołowych)")
    print("wypijasz średnio w ciągu jednej doby?")
    print("1. Mało (poniżej 1 litra - głównie kawa, soki, herbata)")
    print("2. Optymalnie (między 1 a 2 litry)")
    print("3. Dużo (powyżej 2 litrów)")

    user_choice_water = int(input("\nWybierz poziom nawodnienia (1-3): "))

    water_impact = water_mapping.get(user_choice_water, 0.0)

    return water_impact

def years_history(nutrition_data):

    penalty = 0

    print("\n--- TWOJA PRZESZŁOŚĆ METABOLICZNA ---")
    print("Przez ile lat Twoja dieta była bardzo zła (oparta na fast-foodach,")
    print("dużej ilości cukru i wysoko przetworzonym jedzeniu)?")

    years_history = int(input("\nPodaj liczbę lat (jeśli od zawsze jesz zdrowo, wpisz 0): ")) / 10

    if years_history >= 0.6:

        poor_nutrition_decade_penalty = nutrition_data['nutrition_data']['history']['poor_nutrition_decade_penalty']
        penalty = years_history * poor_nutrition_decade_penalty

    finally_penalty = min(penalty, nutrition_data['nutrition_data']['history']['max_history_penalty'])

    return finally_penalty

