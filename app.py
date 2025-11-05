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

# NOTA: aqui os valores em population_ranges estão NA ESCALA "população / 100000"
# ex: 11.45139 representa 11.45139 * 100000 = 1.145.139 habitantes
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
    '9': [10.434252, 11.253503, 11.451245]  # EXEMPLO: usei valores plausíveis (corrija se quiser)
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

# ================== CALCULA UMA VEZ OS PERCENTIS ==================
# Construção do histórico para determinar os percentis do crime_rate
historical_data = []
for y in range(2001, 2024):
    for c in range(10):
        for cr in range(4):
            pop = population_ranges[str(c)][-1]  # pop está em "por 100k"
            # garantir que passamos valores numéricos corretos
            X = [[float(y), float(c), float(pop), float(cr)]]
            pred = model.predict(X)[0]
            historical_data.append(pred)

p20, p40, p60, p80 = np.percentile(historical_data, [20, 40, 60, 80])

# ================== ROTAS ==================
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict_result():
    # Recebe string do form, converte para int
    city_code = int(request.form["city"])
    crime_code = int(request.form['crime'])
    year = int(request.form['year'])

    # Seleção populacional com taxa de crescimento (pop em escala "por 100k")
    if year <= 2009:
        pop = population_ranges[str(city_code)][0]
        base_year, growth_rate = 2001, 0.01
    elif year <= 2021:
        pop = population_ranges[str(city_code)][1]
        base_year, growth_rate = 2010, 0.0015
    else:
        pop = population_ranges[str(city_code)][2]
        base_year, growth_rate = 2022, 0.0015

    # aplica crescimento percentual simples sobre a base (pop ainda "por 100k")
    pop = pop + growth_rate * (year - base_year) * pop  # pop continua sendo "pop/100k"

    # Prepara entrada para o modelo: sempre floats
    X_input = [[float(year), float(city_code), float(pop), float(crime_code)]]
    crime_rate = float(model.predict(X_input)[0])  # valor em "ocorrências por 100k hab."

    # Classificação de status a partir dos percentis pré-calculados
    if crime_rate <= p20:
        crime_status = "Criminalidade Muito Baixa"
    elif crime_rate <= p40:
        crime_status = "Criminalidade Baixa"
    elif crime_rate <= p60:
        crime_status = "Criminalidade Média"
    elif crime_rate <= p80:
        crime_status = "Criminalidade Alta"
    else:
        crime_status = "Criminalidade Muito Alta"

    # Cálculo de casos: crime_rate (por 100k) * pop (pop em unidades de 100k) = casos absolutos
    cases = math.ceil(crime_rate * pop)

    # População absoluta (em número de pessoas)
    population_absolute = int(round(pop * 100000))

    # Retorna template com dados
    return render_template(
        'result.html',
        city_name=city_names[str(city_code)],
        crime_type=crimes_names[str(crime_code)],
        year=year,
        crime_status=crime_status,
        crime_rate=crime_rate,
        cases=cases,
        population=population_absolute,
        color_classes=color_classes,
        emoji_map=emoji_map
    )

if __name__ == '__main__':
    app.run(debug=False)
