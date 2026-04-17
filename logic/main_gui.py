import customtkinter as ctk
from tkinter import messagebox
from data_loader import load_json_data
import datetime
from engine import DeathClockEngine


class DeathClockApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PROGNOZA DŁUGOWIECZNOŚCI v3.0")
        self.geometry("850x650")

        # --- ZMIENNE DANYCH ---
        self.user_name = "Użytkownik"  # Domyślna wartość
        self.current_step = 0

        self.responses = {}

        # Konfiguracja siatki
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Nagłówek i Stopka (jak wcześniej)
        self.setup_ui_static_elements()

        # START: Ekran powitalny
        self.show_welcome_screen()

        self.footer_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.footer_frame.grid(row=3, column=0, sticky="ew")
        self.footer_label = ctk.CTkLabel(self.footer_frame,
                                         text="© 2026 Longevity Engine | Dane oparte na badaniach statystycznych",
                                         font=ctk.CTkFont(size=10))
        self.footer_label.pack(pady=5)

        try:
            self.life_table = load_json_data("life_tables.json")
            self.bmi_risks = load_json_data("bmi_risks.json")
            self.habits_risks = load_json_data("habits_risks.json")
            self.occupations_data = load_json_data("occupations.json")
            self.sleep_data = load_json_data("sleep_tables.json")
            self.social_data = load_json_data("social_relations.json")
            self.environment_data = load_json_data("environment.json")
            self.nutrition_data = load_json_data("nutrition.json")
            self.genetics_data = load_json_data("genetics.json")
            self.stimulants_data = load_json_data("stimulants.json")
            self.subtle_data = load_json_data("subtle_factors.json")

            # Inicjalizacja mapowań (jeśli ich używasz w Etapie IV)
            self.sleep_map = {v['description']: k for k, v in self.sleep_data['sleep_health'].items()}
            self.social_map = {v['description']: k for k, v in self.social_data['social_relations'].items()}
            self.air_map = {v['name']: k for k, v in self.environment_data['environment_data']['current_air'].items()}
            self.noise_map = {v['name']: k for k, v in
                              self.environment_data['environment_data']['current_noise'].items()}
            self.diet_map = {v['name']: k for k, v in self.nutrition_data['nutrition_data']['diet_patterns'].items()}
            self.stim_source_map = {v['name']: k for k, v in self.stimulants_data['caffeine_data']['sources'].items()}
            self.stim_dose_map = {v['name']: k for k, v in self.stimulants_data['caffeine_data']['dosages'].items()}

            # Meta-dane do obliczeń historii
            self.nutri_meta_history = self.nutrition_data['nutrition_data']['history']
            self.subtle_items = self.subtle_data['subtle_data']

        except Exception as e:
            print(f"KRYTYCZNY BŁĄD ŁADOWANIA DANYCH: {e}")
            # Opcjonalnie: wyświetl okno z błędem i zamknij aplikację
            messagebox.showerror("Błąd", f"Nie udało się wczytać plików bazy danych: {e}")


    def setup_ui_static_elements(self):
        # Nagłówek
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.title_label = ctk.CTkLabel(self.header_frame, text="SYSTEM PROGNOZOWANIA DŁUGOWIECZNOŚCI",
                                        font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack()

        # Główny kontener
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        # Pasek postępu (ukryty na ekranie powitalnym)
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=50, pady=(0, 10))
        self.progress_bar.set(0)

    def show_welcome_screen(self):
        self.clear_container()
        self.progress_bar.grid_remove()  # Ukrywamy pasek na wstępie

        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Opis programu
        intro_text = (
            "Witaj w zaawansowanym symulatorze długowieczności.\n\n"
            "Ten program przeanalizuje Twój styl życia, genetykę oraz czynniki środowiskowe, "
            "aby oszacować statystyczną długość Twojego życia.\n\n"
            "Pamiętaj: wynik jest prognozą matematyczną, a nie wyrokiem. "
            "Każda zmiana nawyków może dodać Ci lat!"
        )
        ctk.CTkLabel(frame, text=intro_text, wraplength=500, font=("Arial", 14), justify="center").pack(pady=20)

        # Pole na imię
        ctk.CTkLabel(frame, text="Jak masz na imię?", font=("Arial", 13, "bold")).pack(pady=(20, 5))
        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Twoje imię...", width=250)
        self.name_entry.pack(pady=10)

        # Przycisk start
        ctk.CTkButton(frame, text="ZACZYNAMY", font=("Arial", 14, "bold"),
                      height=40, width=200, command=self.start_survey).pack(pady=30)
        self.bind('<Return>', lambda event: self.start_survey())

    def start_survey(self):
        # Pobieramy imię
        entry_name = self.name_entry.get().strip()
        if entry_name:
            self.user_name = entry_name

        self.progress_bar.grid()  # Pokazujemy pasek postępu
        self.show_step_1()  # Przechodzimy do metryki

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_info(self, title, message):
        # Proste okienko informacyjne (Baza wiedzy)
        info_window = ctk.CTkToplevel(self)
        info_window.title(f"Dlaczego to ważne? - {title}")
        info_window.geometry("400x200")

        label = ctk.CTkLabel(info_window, text=message, wraplength=350, pady=20)
        label.pack()

    def show_step_1(self):
        self.clear_container()
        self.progress_bar.set(0.1)

        # 1. Wczytanie danych z JSON
        try:
            genetics_data = load_json_data("genetics.json")
            gen_section = genetics_data['genetics_data']
            self.longevity_options = {v['name']: k for k, v in gen_section['ancestors_longevity'].items()}
            self.risks_options = {v['name']: k for k, v in gen_section['hereditary_risks'].items()}
        except Exception as e:
            print(f"Błąd ładowania JSON: {e}")
            self.longevity_options = {"Błąd danych": "standard"}
            self.risks_options = {"Błąd danych": "no_risk"}

        # 2. Główny kontener scrollowany
        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Kontener treści (zapewnia marginesy i wyrównanie do lewej)
        main_content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_content.pack(padx=30, fill="x")

        # Powitanie
        ctk.CTkLabel(main_content, text=f"Witaj {self.user_name}!",
                     font=("Arial", 22, "bold"), anchor="w").pack(pady=(10, 5), fill="x")
        ctk.CTkLabel(main_content, text="Zacznijmy od podstaw Twojego profilu biologicznego.",
                     font=("Arial", 12), text_color="gray", anchor="w").pack(pady=(0, 20), fill="x")

        # --- SEKCJA I: METRYKA ---
        ctk.CTkLabel(main_content, text="ETAP I: METRYKA",
                     font=("Arial", 14, "bold"), text_color="#52a5f2", anchor="w").pack(pady=10, fill="x")

        def create_input_row(parent, label_text, info_title, info_text):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(pady=5, fill="x")
            lbl = ctk.CTkLabel(row, text=label_text, width=140, anchor="w", font=("Arial", 12))
            lbl.pack(side="left")
            entry = ctk.CTkEntry(row, width=100)
            entry.pack(side="left", padx=10)
            btn = ctk.CTkButton(row, text="?", width=30, fg_color="#3d3d3d", hover_color="#555555",
                                command=lambda: self.show_info(info_title, info_text))
            btn.pack(side="left")
            return entry

        self.age_entry = create_input_row(main_content, "Wiek:", "Dlaczego pytamy o wiek?",
                                          "Wiek chronologiczny to Twój punkt startowy. Silnik porównuje Twoje dane z oczekiwaną długością życia dla Twojej grupy wiekowej. Pozwala to ocenić, czy Twój styl życia przyspiesza, czy spowalnia Twój zegar biologiczny.")

        self.height_entry = create_input_row(main_content, "Wzrost (cm):", "Znaczenie wzrostu",
                                             "Wzrost w połączeniu z wagą pozwala obliczyć wskaźnik BMI oraz powierzchnię ciała. Dane te są kluczowe do oceny obciążenia serca i układu kostno-stawowego.")

        self.weight_entry = create_input_row(main_content, "Waga (kg):", "Wpływ masy ciała",
                                             "Masa ciała bezpośrednio koreluję z ryzykiem chorób metabolicznych i sercowo-naczyniowych. Nadmiar tkanki tłuszczowej, szczególnie trzewnej, generuje stany zapalne, które przyspieszają starzenie się komórek.")

        # Płeć
        gender_row = ctk.CTkFrame(main_content, fg_color="transparent")
        gender_row.pack(pady=10, fill="x")
        ctk.CTkLabel(gender_row, text="Płeć biologiczna:", width=140, anchor="w", font=("Arial", 12)).pack(side="left")
        self.gender_var = ctk.StringVar(value="M")
        self.gender_switch = ctk.CTkSegmentedButton(gender_row, values=["M", "K"], variable=self.gender_var, width=100)
        self.gender_switch.pack(side="left", padx=10)
        ctk.CTkButton(gender_row, text="?", width=30, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Różnice płciowe",
                                                     "Płeć determinuje gospodarkę hormonalną. Estrogeny u kobiet naturalnie chronią układ krążenia do czasu menopauzy. Statystycznie kobiety żyją dłużej, ale są bardziej podatne na pewne schorzenia, co uwzględnia nasz algorytm.")).pack(
            side="left")

        # --- SEKCJA II: GENETYKA ---
        ctk.CTkLabel(main_content, text="ETAP II: GENETYKA",
                     font=("Arial", 14, "bold"), text_color="#52a5f2", anchor="w").pack(pady=(25, 10), fill="x")

        def create_dropdown_row(parent, label_text, var, options, info_title, info_text):
            lbl = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), anchor="w")
            lbl.pack(pady=(5, 0), fill="x")

            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(pady=2, fill="x")

            menu = ctk.CTkOptionMenu(
                row,
                values=list(options.keys()),
                variable=var,
                width=350,
                height=35,
                fg_color="#1f6aa5",  # Kolor tła przycisku (niebieski)
                button_color="#144870",  # Kolor bocznego przycisku ze strzałką
                button_hover_color="#3281b3",  # Kolor po najechaniu myszką
                dropdown_fg_color="#2b2b2b",  # Kolor tła listy po rozwinięciu
                dropdown_hover_color="#1f6aa5",  # Podświetlenie elementu na liście
                dropdown_text_color="white",  # Kolor tekstu na liście
                font=("Arial", 12)
            )
            menu.pack(side="left")

            btn = ctk.CTkButton(
                row,
                text="?",
                width=35,
                height=35,
                fg_color="#3d3d3d",
                hover_color="#555555",
                command=lambda: self.show_info(info_title, info_text)
            )
            btn.pack(side="left", padx=10)
            return menu

        # Długowieczność
        self.ancestors_var = ctk.StringVar(value=list(self.longevity_options.keys())[2])
        create_dropdown_row(main_content, "Długowieczność przodków (dziadkowie/rodzice):",
                            self.ancestors_var, self.longevity_options,
                            "Dziedziczenie długowieczności",
                            "Genetyka odpowiada za około 25% długości życia. Jeśli Twoi przodkowie żyli wyjątkowo długo, prawdopodobnie posiadasz warianty genów (np. FOXO3), które sprawniej naprawiają uszkodzenia komórkowe i DNA.")

        # Obciążenia
        self.risks_var = ctk.StringVar(value=list(self.risks_options.keys())[2])
        create_dropdown_row(main_content, "Występowanie chorób w rodzinie:",
                            self.risks_var, self.risks_options,
                            "Predyspozycje chorobowe",
                            "Wczesne zawały, udary czy nowotwory u bliskich krewnych mogą wskazywać na dziedziczne osłabienie pewnych układów. Dzięki tej informacji algorytm ocenia poziom ryzyka, który możesz zniwelować odpowiednim stylem życia.")

        # Przycisk nawigacji
        ctk.CTkButton(main_content, text="Zapisz i przejdź do stylu życia",
                      width=300, height=50, font=("Arial", 14, "bold"),
                      command=self.save_step_1).pack(pady=50)


    def save_step_1(self):
        try:
            # 1. Pobieranie danych Metryki
            age_val = self.age_entry.get().strip()
            height_val = self.height_entry.get().strip()
            weight_val = self.weight_entry.get().strip()

            if not all([age_val, height_val, weight_val]):
                messagebox.showwarning("Puste pola", "Wypełnij wiek, wzrost i wagę!")
                return

            # Walidacja i zapis metryki
            self.responses['age'] = int(age_val)
            self.responses['height'] = int(height_val)
            self.responses['weight'] = float(weight_val.replace(",", "."))
            self.responses['gender'] = self.gender_var.get()

            # 2. Pobieranie danych Genetyki (Mapowanie nazwy na klucz JSON)
            chosen_longevity_name = self.ancestors_var.get()
            chosen_risk_name = self.risks_var.get()

            self.responses['gen_ancestors'] = self.longevity_options[chosen_longevity_name]
            self.responses['gen_diseases'] = self.risks_options[chosen_risk_name]

            # Logika zakresów
            if not (1 <= self.responses['age'] <= 120):
                messagebox.showerror("Błąd", "Wiek musi być w przedziale 1-120.")
                return

            print(f"Zapisano dane Etapu I: {self.responses}")
            self.show_step_2()

        except ValueError:
            messagebox.showerror("Błąd danych", "Wiek, wzrost i waga muszą być liczbami!")

    def create_sub_input(self, parent, label_text):
        """Pomocnicza funkcja do tworzenia etykiety i pola wpisywania w jednym wierszu"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(pady=2, fill="x")
        lbl = ctk.CTkLabel(row, text=label_text, width=180, anchor="w")
        lbl.pack(side="left", padx=5)
        entry = ctk.CTkEntry(row, width=80)
        entry.pack(side="left", padx=5)
        return entry

    def show_step_2(self):
        self.clear_container()
        self.progress_bar.set(0.3)

        # GŁÓWNY SCROLLABLE FRAME
        self.scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # NAGŁÓWEK ETAPU
        ctk.CTkLabel(self.scroll_frame, text="ETAP II: STYL ŻYCIA I UŻYWKI",
                     font=("Arial", 18, "bold")).pack(pady=(10, 20))

        # --- SEKCJA: UŻYWKI ---
        nic_group = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        nic_group.pack(pady=5, fill="x", padx=10)

        # Nagłówek sekcji z przyciskiem INFO
        nic_header = ctk.CTkFrame(nic_group, fg_color="transparent")
        nic_header.pack(fill="x", padx=20)
        ctk.CTkLabel(nic_header, text="Używki i nałogi", font=("Arial", 14, "bold"), text_color="#52a5f2").pack(
            side="left")
        ctk.CTkButton(nic_header, text="?", width=30, height=30, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Wpływ używek",
                                                     "Nikotyna i alkohol to silne czynniki mutagenne. Obliczamy 'paczkolata' oraz obciążenie wątroby, "
                                                     "które korelują ze skróceniem telomerów i ryzykiem chorób układu krążenia.")).pack(
            side="left", padx=10)

        # 1. GRUPA PAPIEROSY
        cig_container = ctk.CTkFrame(nic_group, fg_color="transparent")
        cig_container.pack(fill="x", pady=5)
        self.cig_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(cig_container, text="Czy paliłeś/palisz papierosy?", variable=self.cig_var,
                      command=self.toggle_cig).pack(pady=5, padx=20, anchor="w")

        self.cig_frame = ctk.CTkFrame(cig_container, fg_color="transparent")
        self.entry_cig_per_day = self.create_sub_input(self.cig_frame, "Ile sztuk dziennie?")
        self.entry_cig_years = self.create_sub_input(self.cig_frame, "Przez ile lat?")

        self.cig_active_var = ctk.BooleanVar(value=True)
        self.cig_active_check = ctk.CTkCheckBox(self.cig_frame, text="Czy palisz obecnie?",
                                                variable=self.cig_active_var,
                                                command=self.toggle_quit_age_cig)
        self.cig_active_check.pack(pady=5, padx=190, anchor="w")

        self.cig_quit_frame = ctk.CTkFrame(self.cig_frame, fg_color="transparent")
        self.entry_cig_quit_age = self.create_sub_input(self.cig_quit_frame, "W jakim wieku rzuciłeś?")

        # 2. GRUPA VAPE (Analogicznie)
        vape_container = ctk.CTkFrame(nic_group, fg_color="transparent")
        vape_container.pack(fill="x", pady=5)
        self.vape_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(vape_container, text="Czy używałeś/używasz e-papierosy (Vape)?", variable=self.vape_var,
                      command=self.toggle_vape).pack(pady=5, padx=20, anchor="w")

        self.vape_frame = ctk.CTkFrame(vape_container, fg_color="transparent")
        self.entry_vape_years = self.create_sub_input(self.vape_frame, "Przez ile lat?")
        self.vape_active_var = ctk.BooleanVar(value=True)
        self.vape_active_check = ctk.CTkCheckBox(self.vape_frame, text="Czy vapujesz obecnie?",
                                                 variable=self.vape_active_var,
                                                 command=self.toggle_quit_age_vape)
        self.vape_active_check.pack(pady=5, padx=190, anchor="w")

        self.vape_quit_frame = ctk.CTkFrame(self.vape_frame, fg_color="transparent")
        self.entry_vape_quit_age = self.create_sub_input(self.vape_quit_frame, "W jakim wieku rzuciłeś?")

        # 3. GRUPA ALKOHOL
        alko_container = ctk.CTkFrame(nic_group, fg_color="transparent")
        alko_container.pack(fill="x", pady=5)
        self.alko_none_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(alko_container, text="Czy jesteś pełnym abstynentem?", variable=self.alko_none_var,
                      command=self.toggle_alko).pack(pady=5, padx=20, anchor="w")

        self.alko_frame = ctk.CTkFrame(alko_container, fg_color="transparent")
        self.entry_beer = self.create_sub_input(self.alko_frame, "Piwo (500ml/tydz):")
        self.entry_wine = self.create_sub_input(self.alko_frame, "Wino (175ml/tydz):")
        self.entry_vodka = self.create_sub_input(self.alko_frame, "Wódka 40% (50ml/tydz):")
        self.entry_alc50 = self.create_sub_input(self.alko_frame, "Alko 41-50% (50ml/tydz):")
        self.entry_alc75 = self.create_sub_input(self.alko_frame, "Alko 51-75% (50ml/tydz):")

        binge_row = ctk.CTkFrame(self.alko_frame, fg_color="transparent")
        binge_row.pack(fill="x")
        self.binge_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(binge_row, text="Czy pijesz gwałtownie (binge drinking)?", variable=self.binge_var).pack(
            side="left", padx=190)
        ctk.CTkButton(binge_row, text="?", width=25, height=25, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Binge Drinking",
                                                     "Picie gwałtowne (powyżej 5 jednostek w krótkim czasie) jest znacznie groźniejsze dla serca i mózgu niż "
                                                     "taka sama ilość alkoholu rozłożona na cały tydzień.")).pack(
            side="left")

        # --- SEKCJA: SPORT ---
        sport_group = ctk.CTkFrame(self.scroll_frame)
        sport_group.pack(pady=10, fill="x", padx=10)

        sport_header = ctk.CTkFrame(sport_group, fg_color="transparent")
        sport_header.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(sport_header, text="Aktywność fizyczna", font=("Arial", 14, "bold")).pack(side="left")
        ctk.CTkButton(sport_header, text="?", width=30, height=30, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Aktywność a życie",
                                                     "Regularny sport (szczególnie cardio i trening oporowy) obniża wiek biologiczny poprzez poprawę VO2 Max "
                                                     "oraz lepszą wrażliwość na insulinę.\n\n INFO: Podaj lata, w których trenowałeś minimum 3x w tygodniu przez co najmniej 6 miesięcy w roku. Obowiązkowy WF w szkole zazwyczaj nie jest traktowany jako staż sportowy, chyba że wiązał się z dodatkowymi treningami w SKS lub klubie.")).pack(side="left", padx=10)

        self.entry_sport_years = self.create_sub_input(sport_group, "Lata regularnego sportu:")

        # SPOLSZCZONE MENU AKTYWNOŚCI
        self.activity_map = {
            "Siedzący (brak ruchu)": "sedentary",
            "Aktywny (spacer/lekki sport)": "active",
            "Sportowiec (intensywne treningi)": "athlete"
        }

        ctk.CTkLabel(sport_group, text="Obecny poziom aktywności:").pack(pady=(5, 0), padx=25, anchor="w")
        self.activity_lvl_var = ctk.StringVar(value="Aktywny (spacer/lekki sport)")
        self.option_menu = ctk.CTkOptionMenu(sport_group, values=list(self.activity_map.keys()),
                                             variable=self.activity_lvl_var, width=300)
        self.option_menu.pack(pady=10, padx=25, anchor="w")

        # --- PRZYCISKI NAWIGACJI ---
        btn_row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        btn_row.pack(pady=30)
        ctk.CTkButton(btn_row, text="Wstecz", command=self.show_step_1, fg_color="gray", width=120, height=45).pack(
            side="left", padx=10)
        ctk.CTkButton(btn_row, text="Dalej", command=self.save_step_2, width=250, height=45,
                      font=("Arial", 13, "bold")).pack(side="left", padx=10)

        self.toggle_cig()
        self.toggle_vape()
        self.toggle_alko()

    # --- FUNKCJE TOGGLE (POKAZYWANIE/UKRYWANIE) ---
    def toggle_cig(self):
        if self.cig_var.get():
            self.cig_frame.pack(pady=5, padx=20, fill="x")
        else:
            self.cig_frame.pack_forget()

    def toggle_vape(self):
        if self.vape_var.get():
            self.vape_frame.pack(pady=5, padx=20, fill="x")
        else:
            self.vape_frame.pack_forget()

    def toggle_alko(self):
        if self.alko_none_var.get():
            self.alko_frame.pack(pady=5, padx=20, fill="x")
        else:
            self.alko_frame.pack_forget()

    def toggle_quit_age_cig(self):
        if not self.cig_active_var.get():  # Jeśli NIE pali obecnie
            self.cig_quit_frame.pack(fill="x")
        else:
            self.cig_quit_frame.pack_forget()

    def toggle_quit_age_vape(self):
        if not self.vape_active_var.get():  # Jeśli NIE vapuje obecnie
            self.vape_quit_frame.pack(fill="x")
        else:
            self.vape_quit_frame.pack_forget()

    def save_step_2(self):
        try:
            # Resetujemy klucze tytoniowe na wypadek gdyby ktoś odznaczył switch
            self.responses.update({
                'cig_per_day': 0, 'cig_years': 0, 'cig_active': False, 'cig_quit_age': 0,
                'vape_years': 0, 'vape_active': False, 'vape_quit_age': 0
            })

            # Papierosy
            if self.cig_var.get():
                self.responses['cig_per_day'] = int(self.entry_cig_per_day.get() or 0)
                self.responses['cig_years'] = int(self.entry_cig_years.get() or 0)
                self.responses['cig_active'] = self.cig_active_var.get()
                self.responses['cig_quit_age'] = int(
                    self.entry_cig_quit_age.get() or self.responses['age']) if not self.cig_active_var.get() else \
                self.responses['age']

            # Vape
            if self.vape_var.get():
                self.responses['vape_years'] = int(self.entry_vape_years.get() or 0)
                self.responses['vape_active'] = self.vape_active_var.get()
                self.responses['vape_quit_age'] = int(
                    self.entry_vape_quit_age.get() or self.responses['age']) if not self.vape_active_var.get() else \
                self.responses['age']

            # Alkohol
            if not self.alko_none_var.get():
                self.responses.update({
                    'beer': int(self.entry_beer.get() or 0),
                    'wine': int(self.entry_wine.get() or 0),
                    'vodka': int(self.entry_vodka.get() or 0),
                    'alc_50': int(self.entry_alc50.get() or 0),
                    'alc_75': int(self.entry_alc75.get() or 0),
                    'binge': self.binge_var.get()
                })
            else:
                self.responses.update({'beer': 0, 'wine': 0, 'vodka': 0, 'alc_50': 0, 'alc_75': 0, 'binge': False})

            # Aktywność - MAPOWANIE Z POLSKIEGO NA ANGIELSKI KLUCZ
            self.responses['sport_years'] = float(self.entry_sport_years.get().replace(',', '.') or 0)
            self.responses['activity_lvl'] = self.activity_map[self.activity_lvl_var.get()]

            print(f"Zapisano dane Etapu II: {self.responses}")
            self.show_step_3()

        except ValueError:
            messagebox.showerror("Błąd", "W polach liczbowych wpisz tylko cyfry!")

    def show_step_3(self):
        try:
            occ_data = load_json_data("occupations.json")  # Zakładam taką nazwę pliku
            # Mapujemy Nazwa Zawodu -> Klucz techniczny
            self.occ_options = {v['name']: k for k, v in occ_data['occupations'].items()}
        except Exception as e:
            print(f"Błąd occupations.json: {e}")
            self.occ_options = {"Błąd danych": "standard"}

        self.clear_container()
        self.progress_bar.set(0.6)  # Jesteśmy za połową!

        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        main_content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_content.pack(padx=30, fill="x")

        ctk.CTkLabel(main_content, text="ETAP III: PRACA I PSYCHIKA",
                     font=("Arial", 18, "bold"), anchor="w").pack(pady=(10, 5), fill="x")

        # --- WYBÓR ZAWODU ---
        ctk.CTkLabel(main_content, text="Twój zawód / profesja:", font=("Arial", 12, "bold"), anchor="w").pack(
            pady=(20, 0), fill="x")

        occ_row = ctk.CTkFrame(main_content, fg_color="transparent")
        occ_row.pack(pady=5, fill="x")

        self.occ_var = ctk.StringVar(value=list(self.occ_options.keys())[0])
        self.occ_menu = ctk.CTkOptionMenu(
            occ_row,
            values=list(self.occ_options.keys()),
            variable=self.occ_var,
            width=400,
            height=35,
            fg_color="#1f6aa5",
            button_color="#144870"
        )
        self.occ_menu.pack(side="left")

        ctk.CTkButton(occ_row, text="?", width=35, height=35, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Wpływ zawodu",
                                                     "Zawód to nie tylko zarobki, to ekspozycja na pyły, chemia, wysiłek fizyczny lub siedzący tryb życia. Każda branża ma inny współczynnik ryzyka wypadków i chorób zawodowych.")).pack(
            side="left", padx=10)

        # --- POZIOM STRESU (Relatywny) ---
        ctk.CTkLabel(main_content, text="Poziom stresu na tle branży:", font=("Arial", 12, "bold"), anchor="w").pack(
            pady=(20, 5), fill="x")

        stress_desc = ctk.CTkLabel(main_content,
                                   text="Oceń, czy Twoja praca jest bardziej stresująca niż u innych osób na tym samym stanowisku.",
                                   font=("Arial", 11), text_color="gray", anchor="w", justify="left")
        stress_desc.pack(fill="x")

        self.stress_var = ctk.StringVar(value="Typowy")
        self.stress_switch = ctk.CTkSegmentedButton(
            main_content,
            values=["Mniejszy", "Typowy", "Znacznie większy"],
            variable=self.stress_var,
            width=450,
            height=40,
            selected_color="#1f6aa5"
        )
        self.stress_switch.pack(pady=15, anchor="w")

        # Przycisk info dla stresu
        ctk.CTkButton(main_content, text="Dlaczego stres relatywny?", fg_color="gray", height=25,
                      command=lambda: self.show_info("Stres a kortyzol",
                                                     "Przewlekły stres podnosi poziom kortyzolu, co prowadzi do nadciśnienia, bezsenności i degradacji telomerów (końcówek chromosomów). Porównujemy Cię do branży, bo 'stres' chirurga jest inny niż 'stres' bibliotekarza.")).pack(
            pady=5, anchor="w")

        # --- PRZYCISKI NAWIGACJI ---
        btn_row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        btn_row.pack(pady=40)

        # Przycisk Wstecz
        ctk.CTkButton(
            btn_row,
            text="Wstecz",
            command=self.show_step_2,
            fg_color="#3d3d3d",
            hover_color="#2b2b2b",
            width=120,
            height=45
        ).pack(side="left", padx=10)

        # Przycisk Dalej
        ctk.CTkButton(
            btn_row,
            text="Dalej",
            command=self.save_step_3,
            width=250,
            height=45,
            font=("Arial", 13, "bold"),
            fg_color="#1f6aa5"
        ).pack(side="left", padx=10)

    def save_step_3(self):
        # 1. Pobieramy klucz zawodu
        selected_occ_name = self.occ_var.get()
        self.responses['occ_key'] = self.occ_options[selected_occ_name]

        # 2. Mapujemy stres na wartości z Twojego silnika
        stress_map = {
            "Mniejszy": -0.05,
            "Typowy": 0.0,
            "Znacznie większy": 0.10
        }
        self.responses['stress_mod'] = stress_map.get(self.stress_var.get(), 0.0)

        print(f"Zapisano dane Etapu III: {self.responses}")

        # Tutaj wywołamy finałowe obliczenia!
        self.show_step_4()

    def show_step_4(self):
        self.clear_container()
        self.progress_bar.set(0.8)

        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        main_content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_content.pack(padx=30, fill="x")

        ctk.CTkLabel(main_content, text="ETAP IV: REGENERACJA, ŚRODOWISKO I ODŻYWIANIE",
                     font=("Arial", 20, "bold"), anchor="w").pack(pady=(10, 20), fill="x")

        # --- REGENERACJA I RELACJE ---
        self.sleep_var = ctk.StringVar(value=list(self.sleep_map.keys())[2])
        self.create_dropdown_row(main_content, "Czas snu na dobę:", self.sleep_var, self.sleep_map,
                                 "Faza REM i regeneracja",
                                 "Sen to czas usuwania toksyn (system glimfatyczny) z mózgu. Chroniczny brak snu podnosi ryzyko Alzheimera i skraca życie o ok. 10-15%.")

        self.social_var = ctk.StringVar(value=list(self.social_map.keys())[1])
        self.create_dropdown_row(main_content, "Relacje społeczne:", self.social_var, self.social_map,
                                 "Izolacja a biologia",
                                 "Poczucie samotności aktywuje te same ośrodki w mózgu co ból fizyczny. Silne więzi społeczne to jeden z najsilniejszych predyktorów długowieczności (Blue Zones).")

        # --- ŚRODOWISKO ---
        ctk.CTkLabel(main_content, text="ŚRODOWISKO ŻYCIA", font=("Arial", 14, "bold"), text_color="#52a5f2",
                     anchor="w").pack(pady=(20, 5), fill="x")

        self.air_var = ctk.StringVar(value=list(self.air_map.keys())[1])
        self.create_dropdown_row(main_content, "Jakość powietrza:", self.air_var, self.air_map,
                                 "Pyły zawieszone (PM2.5)",
                                 "Drobne pyły przenikają bezpośrednio do krwiobiegu, powodując przewlekły stan zapalny naczyń krwionośnych i uszkadzając serce.")

        self.noise_var = ctk.StringVar(value=list(self.noise_map.keys())[1])
        self.create_dropdown_row(main_content, "Poziom hałasu:", self.noise_var, self.noise_map,
                                 "Zanieczyszczenie hałasem",
                                 "Stały hałas powyżej 55dB (nawet podczas snu) podnosi poziom adrenaliny i kortyzolu, co prowadzi do nadciśnienia tętniczego.")

        # Lata w smogu z przyciskiem INFO
        row_smog = ctk.CTkFrame(main_content, fg_color="transparent")
        row_smog.pack(fill="x", pady=5)
        ctk.CTkLabel(row_smog, text="Ile lat żyłeś w smogu/hałasie?", width=250, anchor="w").pack(side="left")
        self.smog_years_entry = ctk.CTkEntry(row_smog, width=70)
        self.smog_years_entry.insert(0, "0")
        self.smog_years_entry.pack(side="left", padx=10)
        ctk.CTkButton(row_smog, text="?", width=30, height=30, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Efekt kumulacji",
                                                     "Uszkodzenia płuc i układu krążenia kumulują się przez lata. Nawet po przeprowadzce do lasu, organizm potrzebuje dekad na 'odpracowanie' lat w smogu.")).pack(
            side="left")

        # --- ODŻYWIANIE ---
        ctk.CTkLabel(main_content, text="ODŻYWIANIE I METABOLIZM", font=("Arial", 14, "bold"), text_color="#52a5f2",
                     anchor="w").pack(pady=(25, 5), fill="x")

        self.diet_var = ctk.StringVar(value=list(self.diet_map.keys())[2])
        self.create_dropdown_row(main_content, "Twój wzorzec diety:", self.diet_var, self.diet_map,
                                 "Dieta przeciwzapalna",
                                 "Cukier i tłuszcze trans powodują glikację białek – proces 'karmelizowania' Twoich komórek od środka, co przyspiesza starzenie skóry i narządów.")

        # Cukier i Woda z dedykowanymi INFO
        sugar_header = ctk.CTkFrame(main_content, fg_color="transparent")
        sugar_header.pack(fill="x", pady=(15, 2))
        ctk.CTkLabel(sugar_header, text="Spożycie cukru i słodzonych napojów:", font=("Arial", 12, "bold")).pack(
            side="left")
        ctk.CTkButton(sugar_header, text="?", width=25, height=25, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Insulina i IGF-1",
                                                     "Wysoki poziom cukru to ciągle wysoka insulina. Insulina to hormon wzrostu – gdy jest go za dużo, organizm 'rośnie' (tkanka tłuszczowa), zamiast się 'naprawiać'.")).pack(
            side="left", padx=10)

        self.sugar_seg_var = ctk.StringVar(value="Umiarkowanie")
        self.sugar_seg = ctk.CTkSegmentedButton(main_content, values=["Okazjonalnie", "Umiarkowanie", "Często"],
                                                variable=self.sugar_seg_var)
        self.sugar_seg.pack(fill="x", pady=5)

        water_header = ctk.CTkFrame(main_content, fg_color="transparent")
        water_header.pack(fill="x", pady=(15, 2))
        ctk.CTkLabel(water_header, text="Nawodnienie (woda i napary):", font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkButton(water_header, text="?", width=25, height=25, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Homeostaza płynów",
                                                     "Nawodnienie wpływa na gęstość krwi. Odwodnienie zmusza serce do cięższej pracy i spowalnia usuwanie produktów przemiany materii przez nerki.")).pack(
            side="left", padx=10)

        self.water_seg_var = ctk.StringVar(value="Optymalnie")
        self.water_seg = ctk.CTkSegmentedButton(main_content, values=["Mało", "Optymalnie", "Dużo"],
                                                variable=self.water_seg_var)
        self.water_seg.pack(fill="x", pady=5)

        row_history = ctk.CTkFrame(main_content, fg_color="transparent")
        row_history.pack(fill="x", pady=15)
        ctk.CTkLabel(row_history, text="Ile lat Twoja dieta była bardzo zła?", width=250, anchor="w").pack(side="left")
        self.diet_history_entry = ctk.CTkEntry(row_history, width=70)
        self.diet_history_entry.insert(0, "0")
        self.diet_history_entry.pack(side="left", padx=10)
        ctk.CTkButton(row_history, text="?", width=30, height=30, fg_color="#3d3d3d",
                      command=lambda: self.show_info("Pamięć metaboliczna",
                                                     "Długotrwała zła dieta zmienia ekspresję genów (epigenetyka). Nawet po zmianie nawyków, 'blizny metaboliczne' mogą rzutować na zdrowie w starszym wieku. \n\n Co to jest zła dieta? \nZa bardzo złą uznajemy dietę typu zachodniego, czyli:\n"
                                                     "- Jedzenie fast-foodów/gotowych dań min. 3-4 razy w tygodniu.\n"
                                                     "- Regularne picie napojów słodzonych (cola, energetyki).\n"
                                                     "- Duża ilość słodyczy i brak świeżych warzyw.\n\n"
                                                     "Możesz wpisać ułamki, np. 0.5 jeśli taki stan trwał pół roku.")).pack(side="left")

        # --- STYMULANTY ---
        ctk.CTkLabel(main_content, text="STYMULANTY", font=("Arial", 14, "bold"), text_color="#52a5f2",
                     anchor="w").pack(pady=(25, 5), fill="x")

        self.stim_source_var = ctk.StringVar(value=list(self.stim_source_map.keys())[0])
        self.create_dropdown_row(main_content, "Źródło kofeiny:", self.stim_source_var, self.stim_source_map,
                                 "Kofeina vs Energetyki",
                                 "Kawa zawiera polifenole chroniące serce. Napoje energetyczne zawierają sztuczne tauryny i barwniki, które przy dużych dawkach obciążają nerki.")

        self.stim_dose_var = ctk.StringVar(value=list(self.stim_dose_map.keys())[1])
        self.create_dropdown_row(main_content, "Ilość dziennie:", self.stim_dose_var, self.stim_dose_map,
                                 "Dawka śmiertelna i lecznicza",
                                 "Umiarkowana ilość kofeiny (2-3 filiżanki) działa neuroprotekcyjnie. Nadmiar (powyżej 400mg) powoduje arytmię i wypłukuje magnez.")

        # --- NAWIGACJA ---
        btn_row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        btn_row.pack(pady=40)

        ctk.CTkButton(btn_row, text="Wstecz", command=self.show_step_3, fg_color="#3d3d3d", hover_color="#2b2b2b",
                      width=120, height=45).pack(side="left", padx=10)
        ctk.CTkButton(btn_row, text="Dalej", command=self.save_step_4, width=250, height=45, font=("Arial", 13, "bold"),
                      fg_color="#1f6aa5").pack(side="left", padx=10)

    def save_step_4(self):
        try:
            # 1. Mapowanie podstawowych kluczy
            self.responses['sleep_key'] = self.sleep_map[self.sleep_var.get()]
            self.responses['social_key'] = self.social_map[self.social_var.get()]
            self.responses['env_air_key'] = self.air_map[self.air_var.get()]
            self.responses['env_noise_key'] = self.noise_map[self.noise_var.get()]  # ZAPIS HAŁASU
            self.responses['diet_key'] = self.diet_map[self.diet_var.get()]
            self.responses['stim_key'] = self.stim_source_map[self.stim_source_var.get()]
            self.responses['stim_dosage_key'] = self.stim_dose_map[self.stim_dose_var.get()]

            # 2. Pobieranie wartości liczbowych
            smog_years_str = self.smog_years_entry.get().replace(',', '.')
            self.responses['years_in_smog'] = float(smog_years_str or 0)
            diet_years_str = self.diet_history_entry.get().replace(',', '.')
            self.responses['years_penalty_diet'] = float(diet_years_str or 0)

            # 3. Logika segmentów (Cukier i Woda)
            sugar_val = self.sugar_seg_var.get()
            # Mapowanie na wartości, które process_nutrition rozumie (np. 1-3 lub 0/1)
            # Załóżmy: Często = kara, Inne = OK
            self.responses['penalty_sugar'] = 1 if sugar_val == "Często" else 0

            water_val = self.water_seg_var.get()
            # Załóżmy: Mało = kara
            self.responses['penalty_water'] = -1 if water_val == "Mało" else 0

            print(f"Zapisano dane Etapu IV: {self.responses}")
            self.show_step_5()

        except Exception as e:
            messagebox.showerror("Błąd", f"Wpisz poprawne liczby w polach lat! ({e})")


    def create_dropdown_row(self, parent, label_text, var, options, info_title, info_text):
        lbl = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), anchor="w")
        lbl.pack(pady=(15, 2), fill="x")
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x")
        menu = ctk.CTkOptionMenu(row, values=list(options.keys()), variable=var, width=400, height=35,
                                 fg_color="#1f6aa5", button_color="#144870")
        menu.pack(side="left")
        ctk.CTkButton(row, text="?", width=35, height=35, fg_color="#3d3d3d",
                      command=lambda: self.show_info(info_title, info_text)).pack(side="left", padx=10)

    def show_step_5(self):
        self.clear_container()
        self.progress_bar.set(0.95)  # Prawie 100%!

        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        main_content = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        main_content.pack(padx=30, fill="x")

        ctk.CTkLabel(main_content, text="ETAP V: SUBTELNE CZYNNIKI I NAWYKI",
                     font=("Arial", 20, "bold"), anchor="w").pack(pady=(10, 5), fill="x")

        ctk.CTkLabel(main_content, text="Zaznacz wszystkie stwierdzenia, które są prawdziwe w Twoim przypadku:",
                     font=("Arial", 12), text_color="gray", anchor="w").pack(pady=(0, 20), fill="x")

        # Słownik na zmienne przechowujące stan checkboxów
        self.subtle_vars = {}

        # Dynamiczne tworzenie checkboxów na podstawie bazy JSON
        for key, factor in self.subtle_items.items():
            var = ctk.BooleanVar(value=False)
            self.subtle_vars[key] = var

            # Ramka na checkbox i przycisk info
            row = ctk.CTkFrame(main_content, fg_color="transparent")
            row.pack(fill="x", pady=5)

            cb = ctk.CTkCheckBox(row, text=factor['name'], variable=var,
                                 font=("Arial", 12), checkbox_width=22, checkbox_height=22)
            cb.pack(side="left", fill="x", expand=True)

            # Przycisk info (wyjaśniający wpływ danego czynnika)
            impact_text = f"Wpływ: {'+' if factor['impact'] > 0 else ''}{factor['impact']} lat do przewidywanej długości życia."
            ctk.CTkButton(row, text="?", width=30, height=30, fg_color="#3d3d3d",
                          command=lambda t=factor['name'], i=impact_text: self.show_info(t, i)).pack(side="right",
                                                                                                     padx=10)

        # --- PRZYCISK FINALNY ---
        btn_row = ctk.CTkFrame(main_content, fg_color="transparent")
        btn_row.pack(pady=40)

        # 2. Przycisk Wstecz (po lewej)
        ctk.CTkButton(btn_row,
                      text="Wstecz",
                      command=self.show_step_4,
                      fg_color="#3d3d3d",
                      hover_color="#2b2b2b",
                      width=120,
                      height=60,
                      font=("Arial", 14)).pack(side="left", padx=10)

        # 3. Przycisk Finalny (po prawej)
        ctk.CTkButton(btn_row,
                      text="ZAKOŃCZ I OBLICZ DATĘ ŚMIERCI",
                      width=350,
                      height=60,
                      fg_color="#c0392b",
                      hover_color="#a93226",
                      font=("Arial", 14, "bold"),
                      command=self.save_step_5).pack(side="left", padx=10)

    def save_step_5(self):
        # Tworzymy listę wybranych kluczy (dokładnie tak jak w Twoim get_subtle_choice)
        selected_factors = [key for key, var in self.subtle_vars.items() if var.get()]

        self.responses['subtle_choices'] = selected_factors

        print(f"Zapisano dane Etapu V: {self.responses}")
        self.show_final_results()

    def show_final_results(self):
        self.clear_container()
        self.progress_bar.set(1.0)

        try:
            res = self.responses

            # 1. Inicjalizacja silnika
            calculator = DeathClockEngine(
                age=int(res.get('age', 30)),
                gender=res.get('gender', 'M'),
                life_table=self.life_table,
                weight=float(res.get('weight', 70)),
                height=float(res.get('height', 175))
            )

            # 2. Obliczenia szczegółowe
            gen_impact = calculator.process_genetics(res.get('gen_ancestors', 'standard'),
                                                     res.get('gen_diseases', 'no_risk'), self.genetics_data)
            user_bmi, bmi_impact = calculator.bmi(self.bmi_risks)

            nicotine_impact = calculator.process_nicotine(
                res.get('cig_years', 0), res.get('cig_per_day', 0), res.get('cig_active', False),
                res.get('cig_quit_age', 0),
                res.get('vape_years', 0), res.get('vape_active', False), res.get('vape_quit_age', 0),
                self.habits_risks, res.get('stick_per_day', 0), res.get('heat_years', 0),
                res.get('heat_active', False), res.get('heat_quit_age', 0)
            )

            alcohol_impact = calculator.process_alcohol(
                res.get('beer', 0), res.get('wine', 0), res.get('vodka', 0),
                res.get('alc_50', 0), res.get('alc_75', 0),
                self.habits_risks, res.get('gender', 'M'), res.get('binge', False)
            )

            activity_impact = calculator.process_activity(res.get('sport_years', 0), self.habits_risks,
                                                          res.get('activity_lvl', 'sedentary'))
            occ_impact = calculator.process_occupation(res.get('occ_key', 'office'), res.get('stress_mod', 0.0),
                                                       self.occupations_data)
            sleep_impact = calculator.process_sleep(res.get('sleep_key', 'optimal_sleep'), self.sleep_data)
            relation_impact = calculator.process_relation(res.get('social_key', 'average'), self.social_data)
            env_impact = calculator.process_environment(res.get('years_in_smog', 0),
                                                        res.get('env_air_key', 'standard_city'),
                                                        res.get('env_noise_key', 'moderate'), self.environment_data)
            nutri_impact = calculator.process_nutrition(res.get('diet_key', 'balanced'),
                                                        res.get('years_penalty_diet', 0), res.get('penalty_water', 0),
                                                        res.get('penalty_sugar', 0), self.nutrition_data)
            stim_impact = calculator.process_stimulants(res.get('stim_key', 'none'), res.get('stim_dosage_key', 'low'),
                                                        self.stimulants_data)
            subtle_impact = calculator.process_subtle_factors(res.get('subtle_choices', []), self.subtle_data)

            final_age_raw = calculator.calculate_results()
            risk_penalty = calculator.process_statistical_risk(final_age_raw)
            total_final_age = round(final_age_raw + risk_penalty, 1)

            # --- GUI RAPORTU ---
            scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
            scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

            # Nagłówek główny
            self.create_result_header(scroll_frame, total_final_age, user_bmi)

            # --- SEKCJA 1: BIOMETRIA I GENETYKA ---
            f1 = self.create_section_frame(scroll_frame, "BIOMETRIA I DZIEDZICZENIE")
            self.add_report_line(f1, "Twoje BMI", f"{user_bmi:.1f} (Wpływ: {bmi_impact} lat)", "#52a5f2")
            self.add_report_line(f1, "Genetyka", f"Korekta przodków/chorób: {gen_impact} lat")
            self.add_report_line(f1, "Baza (Life Table)",
                                 f"Statystyczna baza dla Twojej płci: {calculator.base_years:.1f} lat")

            # --- SEKCJA 2: NAWYKI I UŻYWKI ---
            f2 = self.create_section_frame(scroll_frame, "ANALIZA STYLU ŻYCIA")
            # Nikotyna szczegółowo
            nic_text = f"{nicotine_impact} lat" if nicotine_impact != 0 else "Brak obciążeń"
            self.add_report_line(f2, "Tytoń/Vape", nic_text, "#e74c3c" if nicotine_impact < 0 else "#2ecc71")

            # Alkohol szczegółowo
            alc_text = f"{alcohol_impact} lat" if alcohol_impact != 0 else "Abstynencja/Znikome"
            self.add_report_line(f2, "Alkohol", alc_text, "#e67e22" if alcohol_impact < -1 else "#2ecc71")

            # Aktywność
            act_color = "#2ecc71" if activity_impact > 0 else "#e74c3c"
            self.add_report_line(f2, "Ruch (Staż: " + str(res.get('sport_years', 0)) + " lat)",
                                 f"{activity_impact} lat", act_color)

            # --- SEKCJA 3: REGENERACJA I ŚRODOWISKO ---
            f3 = self.create_section_frame(scroll_frame, "OTOCZENIE I REGENERACJA")
            self.add_report_line(f3, "Sen", f"{sleep_impact} lat", "#2ecc71" if sleep_impact >= 0 else "#e74c3c")
            self.add_report_line(f3, "Relacje społeczne", f"{relation_impact} lat")
            self.add_report_line(f3, "Praca i Stres", f"Zawód: {res.get('occ_key', 'office')} ({occ_impact} lat)")
            self.add_report_line(f3, "Środowisko",
                                 f"Smog/Hałas: {env_impact} lat (Lata w smogu: {res.get('years_in_smog', 0)})")

            # --- SEKCJA 4: METABOLIZM I ODŻYWIANIE ---
            f4 = self.create_section_frame(scroll_frame, "METABOLIZM I DIETA")
            nutri_txt = f"{nutri_impact} lat (Błędy z przeszłości: {res.get('years_penalty_diet', 0)} lat)"
            self.add_report_line(f4, "Wzorzec diety", nutri_txt)

            if res.get('penalty_sugar', 0) > 0:
                self.add_report_line(f4, "! Cukier", "Wykryto wysoką podaż cukru (kara HR)", "#e74c3c")
            if res.get('penalty_water', 0) < 0:
                self.add_report_line(f4, "! Nawodnienie", "Niedostateczna ilość płynów", "#e67e22")

            self.add_report_line(f4, "Stymulanty", f"Kofeina/Energeryki: {stim_impact} lat")

            # --- SEKCJA 5: CZYNNIKI DODATKOWE ---
            f5 = self.create_section_frame(scroll_frame, "PODSUMOWANIE STATYSTYCZNE")
            self.add_report_line(f5, "Czynniki subtelne", f"+{subtle_impact} lat", "#2ecc71")
            self.add_report_line(f5, "Ryzyko losowe", f"{risk_penalty} lat", "gray")

            # Przycisk zamknięcia
            ctk.CTkButton(scroll_frame, text="ZAKOŃCZ ANALIZĘ", width=300, height=50,
                          fg_color="#3d3d3d", command=self.destroy).pack(pady=40)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            messagebox.showerror("Błąd Raportu", f"Wystąpił problem podczas generowania danych: {e}")

    # --- METODY POMOCNICZE DLA WYGLĄDU ---

    def create_result_header(self, parent, age, bmi):
        header = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=15)
        header.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(header, text="TWÓJ PRZEWIDYWANY WIEK DOŻYCIA", font=("Arial", 16)).pack(pady=(20, 0))
        ctk.CTkLabel(header, text=f"{age} LAT", font=("Arial", 72, "bold"), text_color="#c0392b").pack(pady=10)
        ctk.CTkLabel(header, text=f"Twoje BMI: {bmi:.1f}", font=("Arial", 14, "italic"), text_color="gray").pack(
            pady=(0, 20))

    def add_report_line(self, parent, title, value, color="white"):
        line = ctk.CTkFrame(parent, fg_color="transparent")
        line.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(line, text=title, font=("Arial", 11, "bold"), text_color="#52a5f2", width=180, anchor="w").pack(
            side="left")
        ctk.CTkLabel(line, text=value, font=("Arial", 12), text_color=color, anchor="w", justify="left").pack(
            side="left", fill="x", expand=True)

        # Mała linia oddzielająca (opcjonalnie)
        ctk.CTkFrame(parent, height=1, fg_color="#333333").pack(fill="x", padx=10)

    def create_section_frame(self, parent, title):
        container = ctk.CTkFrame(parent, fg_color="#1e1e1e", corner_radius=10)
        container.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(container, text=title, font=("Arial", 12, "bold"), text_color="#52a5f2").pack(pady=(10, 5),
                                                                                                   padx=15, anchor="w")
        return container

    def restart_app(self):
        """Resetuje wszystkie dane i wraca do Etapu I"""
        self.responses = {}
        self.show_step_1()

if __name__ == "__main__":
    app = DeathClockApp()
    app.mainloop()