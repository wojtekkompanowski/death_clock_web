def get_occupation_choice(occupations_data):
    # Mapowanie Twoich dokładnych kluczy z JSON do kategorii
    categories = {
        "1": ("IT, Technologia i Design", [
            "software_engineer", "frontend_dev", "backend_dev", "fullstack_dev",
            "devops", "data_scientist", "data_analyst", "cybersecurity",
            "qa_tester", "it_support", "ux_designer", "graphic_designer", "game_dev"
        ]),
        "2": ("Medycyna i Pomoc Społeczna", [
            "doctor", "surgeon", "anesthesiologist", "nurse", "paramedic",
            "pharmacist", "dentist", "physiotherapist", "psychologist",
            "psychiatrist", "social_worker"
        ]),
        "3": ("Służby i Bezpieczeństwo", [
            "police", "detective", "firefighter", "soldier", "security_guard"
        ]),
        "4": ("Budownictwo, Przemysł i Inżynieria", [
            "construction_worker", "electrician", "plumber", "welder", "carpenter",
            "bricklayer", "roofer", "miner", "factory_worker", "machine_operator",
            "civil_engineer", "mechanical_engineer"
        ]),
        "5": ("Transport, Logistyka i Lotnictwo", [
            "truck_driver", "bus_driver", "taxi_driver", "courier",
            "warehouse_worker", "forklift_operator", "pilot",
            "flight_attendant", "air_traffic_controller"
        ]),
        "6": ("Prawo, Edukacja i Administracja", [
            "lawyer", "judge", "prosecutor", "teacher", "kindergarten_teacher",
            "professor", "accountant", "auditor", "banker", "hr",
            "recruiter", "manager"
        ]),
        "7": ("Handel, Usługi i Gastronomia", [
            "retail_worker", "cashier", "store_manager", "call_center",
            "chef", "waiter", "bartender", "cleaner", "janitor"
        ]),
        "8": ("Nauka, Media i Rolnictwo", [
            "biologist", "chemist", "physicist", "journalist",
            "editor", "photographer", "farmer", "gardener"
        ])
    }

    print("\n--- WYBÓR KATEGORII ZAWODOWEJ ---")
    for key, val in categories.items():
        print(f"{key}. {val[0]}")

    cat_choice = input("\nWybierz kategorię (numer): ")

    if cat_choice in categories:
        selected_cat_name, job_keys = categories[cat_choice]
        print(f"\n--- Zawody w kategorii: {selected_cat_name} ---")

        for i, key in enumerate(job_keys, 1):
            # Pobieramy nazwę z Twojego JSONa
            job_name = occupations_data['occupations'][key]['name']
            print(f"{i}. {job_name}")

        try:
            job_idx = int(input("\nWybierz numer zawodu: ")) - 1
            if 0 <= job_idx < len(job_keys):
                return job_keys[job_idx]
            else:
                print("Nieprawidłowy numer. Wybrano domyślnie: Programista.")
                return "software_engineer"
        except ValueError:
            print("To nie jest liczba. Wybrano domyślnie: Programista.")
            return "software_engineer"

    print("Nieprawidłowy wybór kategorii. Wybrano domyślnie: Programista.")
    return "software_engineer"