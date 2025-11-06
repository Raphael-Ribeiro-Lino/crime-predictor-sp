from flask import Flask, request, render_template
import pickle
import math
import numpy as np

app = Flask(__name__)

# --- Filtro personalizado para formato brasileiro ---
@app.template_filter('brnum')
def brnum(value):
    try:
        return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value

# ================== MODELO ==================
model = pickle.load(open('Model/model.pkl', 'rb'))

# ================== DADOS FIXOS ==================
city_names = {
    '0': 'Campinas',
    '1': 'Guarulhos',
    '2': 'Osasco',
    '3': 'Ribeirão Preto',
    '4': 'Santo André',
    '5': 'Sorocaba',
    '6': 'São Bernardo do Campo',
    '7': 'São José do Rio Preto',
    '8': 'São José dos Campos',
    '9': 'São Paulo'
}

crimes_names = {
    '0': 'Homicidio Doloso',
    '1': 'Furto',
    '2': 'Roubo',
    '3': 'Furto e Roubo de Veiculo'
}

# População (em unidades de 100 mil habitantes)
population_ranges = {
    '0': [9.69396, 10.80999, 11.38309],
    '1': [10.72717, 12.21979, 12.91771],
    '2': [6.52593, 6.66469, 7.28615],
    '3': [5.04923, 6.05114, 6.98259],
    '4': [6.49331, 6.76407, 7.48919],
    '5': [4.93468, 5.86311, 7.23574],
    '6': [7.03177, 7.65463, 8.10729],
    '7': [3.58523, 4.08435, 4.80439],
    '8': [5.39313, 6.27544, 6.97428],
    '9': [104.34252, 112.53503, 114.51245]  # Corrigido (São Paulo)
}

# ================== MAPEAMENTO DE CORES E EMOJIS ==================
color_classes = {
    "Criminalidade Muito Baixa": "crime-baixa-2",
    "Criminalidade Baixa": "crime-baixa",
    "Criminalidade Média": "crime-media",
    "Criminalidade Alta": "crime-alta",
    "Criminalidade Muito Alta": "crime-alta-2"
}

emoji_map = {
    "Criminalidade Muito Baixa": "🟢",
    "Criminalidade Baixa": "🟡",
    "Criminalidade Média": "🟤",
    "Criminalidade Alta": "🟠",
    "Criminalidade Muito Alta": "🔴"
}

# ================== MÉDIAS NACIONAIS (por 100 mil hab.) ==================
national_avg = {
    '0': 18,   # Homicídio Doloso
    '1': 400,  # Furto
    '2': 350,  # Roubo
    '3': 178   # Furto e Roubo de Veículo
}

# ================== ROTAS ==================
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict_result():
    city_code = request.form["city"]
    crime_code = request.form["crime"]
    year = int(request.form["year"])

    # Seleciona base populacional e crescimento
    if year <= 2009:
        pop = population_ranges[city_code][0]
        base_year, growth_rate = 2001, 0.01
    elif year <= 2021:
        pop = population_ranges[city_code][1]
        base_year, growth_rate = 2010, 0.0015
    else:
        pop = population_ranges[city_code][2]
        base_year, growth_rate = 2022, 0.0015

    # População real (em pessoas)
    pop_real = pop * 100000
    pop_real = pop_real * (1 + growth_rate * (year - base_year))
    pop_for_model = pop_real / 100000  # volta à escala do modelo

    # Predição
    X_input = [[float(year), float(city_code), float(pop_for_model), float(crime_code)]]
    crime_rate = float(model.predict(X_input)[0])  # valor em ocorrências por 100 mil hab.

    # ================== CLASSIFICAÇÃO (MÉDIAS NACIONAIS - 2024) ==================
    if crime_code == '0':  # Homicídio Doloso
        if crime_rate <= 10:
            crime_status = "Criminalidade Muito Baixa"
        elif crime_rate <= 18:
            crime_status = "Criminalidade Baixa"
        elif crime_rate <= 30:
            crime_status = "Criminalidade Média"
        elif crime_rate <= 50:
            crime_status = "Criminalidade Alta"
        else:
            crime_status = "Criminalidade Muito Alta"

    elif crime_code == '1':  # Furto
        if crime_rate <= 200:
            crime_status = "Criminalidade Muito Baixa"
        elif crime_rate <= 400:
            crime_status = "Criminalidade Baixa"
        elif crime_rate <= 700:
            crime_status = "Criminalidade Média"
        elif crime_rate <= 1000:
            crime_status = "Criminalidade Alta"
        else:
            crime_status = "Criminalidade Muito Alta"

    elif crime_code == '2':  # Roubo
        if crime_rate <= 150:
            crime_status = "Criminalidade Muito Baixa"
        elif crime_rate <= 350:
            crime_status = "Criminalidade Baixa"
        elif crime_rate <= 600:
            crime_status = "Criminalidade Média"
        elif crime_rate <= 900:
            crime_status = "Criminalidade Alta"
        else:
            crime_status = "Criminalidade Muito Alta"

    elif crime_code == '3':  # Furto e Roubo de Veículo
        if crime_rate <= 80:
            crime_status = "Criminalidade Muito Baixa"
        elif crime_rate <= 178:
            crime_status = "Criminalidade Baixa"
        elif crime_rate <= 300:
            crime_status = "Criminalidade Média"
        elif crime_rate <= 500:
            crime_status = "Criminalidade Alta"
        else:
            crime_status = "Criminalidade Muito Alta"

    # Casos absolutos
    cases = math.ceil(crime_rate * pop_for_model)

    # Texto comparativo (opcional)
    avg = national_avg[crime_code]
    if crime_rate > avg:
        comparativo = f"acima da média nacional de {avg} por 100 mil hab."
    elif crime_rate < avg:
        comparativo = f"abaixo da média nacional de {avg} por 100 mil hab."
    else:
        comparativo = f"igual à média nacional de {avg} por 100 mil hab."

    # Retorna para o template
    return render_template(
        'result.html',
        city_name=city_names[city_code],
        crime_type=crimes_names[crime_code],
        year=year,
        crime_status=crime_status,
        crime_rate=crime_rate,
        cases=cases,
        population=int(round(pop_real)),
        color_classes=color_classes,
        emoji_map=emoji_map,
        comparativo=comparativo
    )

if __name__ == '__main__':
    app.run(debug=False)
