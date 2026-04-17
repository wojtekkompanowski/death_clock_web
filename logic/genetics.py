def get_genetics_ancestors(genetics_data, choice_key):
    # Wyciągamy sekcję z danymi
    genetics_section = genetics_data['genetics_data']
    ancestors_data = genetics_section['ancestors_longevity']

    # Sprawdzamy czy klucz istnieje, jeśli nie - zwracamy 0
    if choice_key in ancestors_data:
        return ancestors_data[choice_key]
    return 0

def get_genetic_diseases(genetics_data, choice_key):
    genetics_section = genetics_data['genetics_data']
    diseases_data = genetics_section['hereditary_risks']

    if choice_key in diseases_data:
        return diseases_data[choice_key]
    return 0

