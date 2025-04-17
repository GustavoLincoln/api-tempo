from flask import Flask, jsonify
import requests
import redis
import json

app = Flask(__name__)

# Conexão com Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/recommendation/<city>')
def get_recommendation(city):
    try:
        # Tenta buscar no cache
        cached = r.get(city)
        if cached:
            data = json.loads(cached)
        else:
            response = requests.get(f'http://localhost:3001/weather/{city}')
            if response.status_code != 200:
                return jsonify({"error": "Cidade não encontrada"}), 404
            data = response.json()
            r.setex(city, 60, json.dumps(data))  # cache por 60s

        temp = data["temp"]
        recommendation = ""

        if temp > 30:
            recommendation = "Está quente! Beba água e use protetor solar."
        elif temp > 15:
            recommendation = "Clima agradável! Aproveite o dia."
        else:
            recommendation = "Está frio! Leve um casaco."

        return jsonify({
            "city": data["city"],
            "temp": temp,
            "recommendation": recommendation
        })
    except Exception as e:
        print(e)
        return jsonify({"error": "Erro interno"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
