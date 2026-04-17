def get_sleep_choice(sleep_data):

    selected_sleep = None

    sleep_menu = {
        "1": "short_sleep",
        "2": "borderline_sleep",
        "3": "optimal_sleep",
        "4": "long_sleep"
    }

    print("\n--- WYBÓR ILOŚCI SNU ---")
    for key, val in sleep_menu.items():
        print(f"{key}. {val}")

    choice = input("\nPodaj numer: ")

    if choice in sleep_menu:
        selected_sleep = sleep_menu[choice]

    return selected_sleep