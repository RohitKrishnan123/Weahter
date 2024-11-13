import os
from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("city")
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")  # Get API key from environment variable
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            json_data = requests.get(api).json()
            if json_data.get("cod") != 200:
                return jsonify({"error": f"City '{city}' not found."}), 404

            # Extract weather information
            condition = json_data['weather'][0]['main']
            icon = json_data['weather'][0]['icon']
            temp = int(json_data['main']['temp'] - 273.15)
            min_temp = int(json_data['main']['temp_min'] - 273.15)
            max_temp = int(json_data['main']['temp_max'] - 273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            sunset = time.strftime('%I:%M %p', time.gmtime(json_data['sys']['sunrise'] - 21600))
            sunrise = time.strftime('%I:%M %p', time.gmtime(json_data['sys']['sunset'] - 21600))

            return render_template("index.html", city=city, condition=condition, icon=icon, temp=temp, min_temp=min_temp, 
                                   max_temp=max_temp, pressure=pressure, humidity=humidity, wind=wind, sunrise=sunrise, sunset=sunset)
        except Exception:
            return jsonify({"error": "Failed to retrieve data."}), 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

