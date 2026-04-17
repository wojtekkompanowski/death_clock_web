def get_environment_air_choice(environment_data):

    environment_section = environment_data['environment_data']

    environment_key = environment_section['current_air']

    air_keys_list = list(environment_key.keys())

    print("\n--- WYBÓR JAKOŚCI POWIETRZA W TWOIM OBECNYM ZAMIESZKANIU ---")
    for i, val in enumerate(environment_key.values(), start=1):
        print(f"{i}, {val['name']}")

    choice = int(input("Wybierz obecne miejsce zamieszkania: ")) - 1
    selected_key = air_keys_list[choice]

    print(selected_key)
    return selected_key

def get_environment_noise_choice(environment_data):

    environment_section = environment_data['environment_data']

    environment_key = environment_section['current_noise']

    noise_keys_list = list(environment_key.keys())

    print("\n--- WYBÓR STOPNIA HAŁASU W TWOIM OBECNYM ZAMIESZKANIU ---")
    for i, val in enumerate(environment_key.values(), start=1):
        print(f"{i}. {val['name']}")

    choice = int(input("Wybierz obecny hałas w twoim miejscu zamieszkania: ")) - 1
    selected_key = noise_keys_list[choice]

    print(selected_key)
    return selected_key

