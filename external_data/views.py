import requests

import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render


def dashboard(request):
    weather_data = {}
    chart_uri = None

    try:
        lat, lon = 54.5189, 18.5305
        meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&timezone=Europe%2FWarsaw"

        response = requests.get(meteo_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        times = data['hourly']['time'][:24]
        temps = data['hourly']['temperature_2m'][:24]

        formatted_times = [t.split('T')[1] for t in times]

        weather_data = {
            'current_temp': temps[0],
            'city': 'Gdynia'
        }

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(formatted_times, temps, marker='o', color='#007BFF')
        ax.set_title("Prognoza temperatury na najbliższe 24h w Gdynii")
        ax.set_xlabel("Godzina")
        ax.set_ylabel("Temperatura (°C)")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        chart_uri = urllib.parse.quote(string)
        plt.close(fig)

    except requests.exceptions.RequestException as e:
        weather_data['error'] = f"Błąd pobierania danych pogodowych: {e}"

    context = {
        'weather': weather_data,
        'chart_uri': chart_uri,
    }

    return render(request, 'external_data/dashboard.html', context)
