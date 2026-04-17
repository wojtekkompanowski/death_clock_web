def get_subtle_choice(subtle_data):
    choices = {}
    print("\n--- CZYNNIKI SUBTELNE (UKRYTE) ---")

    for key, value in subtle_data['subtle_data'].items():
        any = input(f"{value['name']} (tak/nie): ").lower()
        choices[key] = True if any == "t" else False

    return choices