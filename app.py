from flask import Flask, request, render_template 
import pickle 
import math

model = pickle.load(open('Model/model.pkl', 'rb')) 

app = Flask(__name__) 

@app.route('/') 
def index(): 
    return render_template("index.html") 

@app.route('/predict', methods=['POST']) 
def predict_result(): 
    
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
    
    # População em diferentes períodos [2001-2009, 2010-2021, 2022-2024]
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
    '9': [104.34252, 112.53503, 114.51245]
}

    
    city_code = request.form["city"] 
    crime_code = request.form['crime'] 
    year = int(request.form['year']) 
    
    # Seleciona a população com base no ano
    if year <= 2009:
        pop = population_ranges[city_code][0]
        base_year = 2001
        growth_rate = 0.01  # 1% ao ano
    elif year <= 2021:
        pop = population_ranges[city_code][1]
        base_year = 2010
        growth_rate = 0.0015  # 0,15% ao ano
    elif year <= 2023:
        pop = population_ranges[city_code][2]
        base_year = 2022
        growth_rate = 0.0015  # 0,15% ao ano
    else:  # Ano >= 2024
        pop = population_ranges[city_code][2]
        base_year = 2022
        growth_rate = 0.0015  # 0,15% ao ano
    
    year_diff = year - base_year
    pop = pop + growth_rate * year_diff * pop
    print(f"A população usada para {city_names[city_code]} no ano {year} é: {pop}")
    crime_rate = model.predict([[year, city_code, pop, crime_code]])[0] 
    print(f"A taxa de criminalidade do modelo é {crime_rate}")
    city_name = city_names[city_code] 
    crime_type = crimes_names[crime_code] 
    
    if crime_rate <= 1:
        crime_status = "Criminalidade Muito Baixa" 
    elif crime_rate <= 5:
        crime_status = "Criminalidade Baixa"
    elif crime_rate <= 15:
        crime_status = "Criminalidade Muito Alta"
    else:
        crime_status = "Criminalidade Muito Alta" 
    
    cases = math.ceil(crime_rate * pop)
    
    return render_template(
        'result.html',
        city_name=city_name,
        crime_type=crime_type,
        year=year,
        crime_status=crime_status,
        crime_rate=crime_rate,
        cases=cases,
        population=pop*100000
    )

if __name__ == '__main__':
    app.run(debug=False)
