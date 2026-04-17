def get_stimulants_choice(stimulants_data):

    stimulants_key = stimulants_data['caffeine_data']

    stimulants_sources = stimulants_key['sources']

    stimulants_keys = list(stimulants_sources.keys())


    print("\n--- WYBÓR SPOŻYWANEJ KOFEINY DZIENNIE ---")

    for i, val in enumerate(stimulants_sources.values(), start=1):
        print(f"{i}. {val['name']}")

    choice = int(input("W jaki sposób dostarczasz kofeinę do organizmu? ")) - 1
    choice_key = stimulants_keys[choice]

    return choice_key

def get_stimulants_dosages(stimulants_data):

    stimulants_key = stimulants_data['caffeine_data']

    stimulants_dosages = stimulants_key['dosages']

    stimulants_keys = list(stimulants_dosages.keys())

    print("\n--- WYBÓR SPOŻYWANEJ ILOŚCI KOFEINY DZIENNIE ---")

    for i, val in enumerate(stimulants_dosages.values(), start=1):
        print(f"{i}. {val['name']}")

    choice = int(input("Ile kofeiny spożywasz dziennie? ")) - 1
    choice_key = stimulants_keys[choice]


    return choice_key


