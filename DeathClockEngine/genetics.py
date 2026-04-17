def get_genetics_ancestors(genetics_data):
    genetics_section = genetics_data['genetics_data']

    genetics_key = genetics_section['ancestors_longevity']

    genetics_keys_list = list(genetics_key.keys())

    print("\n--- WYBÓR DŁUGOWIECZNOŚCI PRZODKÓW ---")
    for i, val in enumerate(genetics_key.values(), start=1):
        print(f"{i}. {val['name']}")

    choice = int(input("Wybierz długowieczność twojej rodziny: ")) - 1

    genetic_choice = genetics_keys_list[choice]

    return genetic_choice

def get_genetic_diseases(genetics_data):

    genetics_section = genetics_data['genetics_data']

    genetics_key = genetics_section['hereditary_risks']

    genetics_key_list = list(genetics_key.keys())

    print("\n--- WYBÓR OBCIĄŻEŃ DZIEDZICZNYCH ---")
    for i, val in enumerate(genetics_key.values(), start=1):
        print(f"{i}. {val['name']}")

    choice = int(input("Wybierz obciążenia genetyczne w twojej rodzinie: ")) - 1

    genetic_choice = genetics_key_list[choice]

    return genetic_choice

