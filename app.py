from flask import Flask, request, jsonify, render_template
from logic.data_loader import load_json_data
from logic.engine import DeathClockEngine
import os

app = Flask(__name__)

life_table = load_json_data("life_tables.json")
bmi_risks = load_json_data("bmi_risks.json")
habits_risks = load_json_data("habits_risks.json")
occupations_data = load_json_data("occupations.json")
sleep_data = load_json_data("sleep_tables.json")
social_data = load_json_data("social_relations.json")
environment_data = load_json_data("environment.json")
nutrition_data = load_json_data("nutrition.json")
genetics_data = load_json_data("genetics.json")
stimulants_data = load_json_data("stimulants.json")
subtle_data = load_json_data("subtle_factors.json")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_all', methods=['POST'])
def handle_base_data():
    data = request.json

    print("\n--- ODEBRANO PACZKĘ Z JS ---")
    print(data)
    print("---------------------------\n")

    # Sprawdź czy klucze w ogóle istnieją
    age = data.get('age')
    anc = data.get('ancestors_choice')
    dis = data.get('diseases_choice')
    print(f"DEBUG: Wiek={age}, Przodkowie={anc}, {dis}")

    engine = DeathClockEngine(
        age=int(data['age']),
        gender=data['gender'],
        life_table=life_table,
        weight=float(data['weight']),
        height=float(data['height'])
    )

    gen_impact = engine.process_genetics(
        data['ancestors_choice'],
        data['diseases_choice'],
        genetics_data
    )

    nicotine_impact = engine.process_nicotine(
        cig_years=data['cig_years'],
        cig_per_day=data['cig_per_day'],
        cig_active=data['cig_active'],
        cig_quit_age=data['cig_quit_age'],
        vape_years=data['vape_years'],
        vape_active=data['vape_active'],
        vape_quit_age=data['vape_quit_age'],
        habits_risks=habits_risks, # Ten JSON wczytany na początku app.py
        stick_per_day=data['stick_per_day'],
        heat_years=data['heat_years'],
        heat_active=data['heat_active'],
        heat_quit_age=data['heat_quit_age'])

    alcohol_impact = engine.process_alcohol(
        beer_quantity=data['beer_quantity'],
        wine_quantity=data['wine_quantity'],
        vodka_quantity=data['vodka_quantity'],
        alcohol_50_quantity=data['alcohol_50_quantity'],
        alcohol_75_quantity=data['alcohol_75_quantity'],
        habits_risks=habits_risks,
        gender=data['gender'],
        binge_drinking=data['binge_drinking'])

    activity_impact = engine.process_activity(
        year_activity=data['year_activity'],
        habits_risks=habits_risks,
        current_level=data['current_level']
    )

    occ_impact = engine.process_occupation(
        occ_key=data['occ_key'],
        stress_modifier=data['stress_modifier'],
        occupations_data=occupations_data
    )
    sleep_impact = engine.process_sleep(
        sleep_key=data['sleep_key'],
        sleep_data=sleep_data
    )
    relations_impact = engine.process_relation(
        relation_keys=data['relation_keys'],
        social_data=social_data
    )
    environment_impact = engine.process_environment(
        years_in_smog=data['years_in_smog'],
        environment_air_key=data['environment_air_key'],
        environment_noise_key=data['environment_noise_key'],
        environment_data=environment_data
    )

    nutrition_impact = engine.process_nutrition(
        data, nutrition_data
    )

    stimulants_impact = engine.process_stimulants(
        data, stimulants_data
    )

    subtle_factors_impact = engine.process_subtle_factors(
       choices=data['subtle_choices'],
        subtle_data=subtle_data
    )

    user_bmi, bmi_impact = engine.bmi(bmi_risks)

    final_age = engine.calculate_results()
    print(f"Finałowa czysta: {final_age}")
    risk_penalty = engine.process_statistical_risk(final_age)

    print(f"ryzyko kara: {risk_penalty}")

    final_age += risk_penalty

    print(f"Fianłowa po odjeciu ryzyka: {final_age}")
    final_age += subtle_factors_impact

    print(f"Finałowa po odjeciu subtle: {final_age}")

    return jsonify({
        "status": "success",
        "predicted_age": round(final_age, 1),
        "bmi": user_bmi,
        "bmi_impact": round(bmi_impact, 2),
        "genetics_total_impact": round(gen_impact, 2),
        "nicotine_impact": round(nicotine_impact, 2),
        "alcohol_impact": round(alcohol_impact, 2),
        "activity_impact": round(activity_impact, 2),
        "occ_impact": round(occ_impact, 2),
        "sleep_impact": round(sleep_impact, 2),
        "relations_impact": round(relations_impact, 2),
        "environment_impact": round(environment_impact, 2),
        "nutrition_impact": round(nutrition_impact, 2),
        "stimulants_impact": round(stimulants_impact, 2),
        "subtle_factors_impact": round(subtle_factors_impact, 2)
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)