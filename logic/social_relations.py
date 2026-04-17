def get_social_relations_choice(social_relations_data):

    print("\n--- WYBÓR RELACJI SPOŁECZNYCH ---")

    relations_section = social_relations_data['social_relations']

    relations_key = list(relations_section.keys())


    for i, key in enumerate(relations_key, start=1):
        description = relations_section[key]['description']
        print(f'{i}. {description}')

    choice = int(input("Wybierz poziom relacji (1-3): ")) - 1
    selected_key = relations_key[choice]

    return selected_key
