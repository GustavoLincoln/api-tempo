from flask import Flask, jsonify

app = Flask(__name__)

weather_data = {
    "SãoPaulo": {"city": "São Paulo", "temp": 25, "unit": "Celsius"},
    "RioDeJaneiro": {"city": "Rio de Janeiro", "temp": 34, "unit": "Celsius"},
    "Curitiba": {"city": "Curitiba", "temp": 12, "unit": "Celsius"},
}

@app.route('/weather/<city>')
def get_weather(city):
    data = weather_data.get(city)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Cidade não encontrada"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)
