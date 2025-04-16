# api_a.py
from flask import Flask, jsonify
import requests
from functools import lru_cache

app = Flask(__name__)

API_B_URL = "http://localhost:5001/weather"

@lru_cache(maxsize=10)
def get_weather_from_api_b(city):
    try:
        response = requests.get(f"{API_B_URL}/{city}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    weather = get_weather_from_api_b(city)
    if not weather:
        return jsonify({"error": "Não foi possível obter os dados da cidade."}), 404

    temp = weather["temp"]
    
    if temp > 30:
        advice = "Está muito quente! Beba água e use protetor solar."
    elif temp > 15:
        advice = "O clima está agradável, aproveite o dia!"
    else:
        advice = "Está frio! Vista um casaco."

    return jsonify({
        "city": weather["city"],
        "temperature": temp,
        "unit": weather["unit"],
        "advice": advice
    })

if __name__ == '__main__':
    app.run(port=5000)
