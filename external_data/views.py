import requests

import matplotlib.pyplot as plt
import io
import urllib
import base64
from django.shortcuts import render
from django.http import JsonResponse


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

    users_stats = []
    try:
        users_res = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5)
        posts_res = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=5)

        users_res.raise_for_status()
        posts_res.raise_for_status()

        users = users_res.json()
        posts = posts_res.json()

        for user in users[:5]:
            user_posts = [p for p in posts if p['userId'] == user['id']]

            avg_title_length = sum(len(p['title']) for p in user_posts) / len(user_posts) if user_posts else 0

            users_stats.append({
                'name': user['name'],
                'post_count': len(user_posts),
                'avg_title_length': round(avg_title_length, 1)
            })

    except requests.exceptions.RequestException as e:
        users_stats = [{'error': f"Błąd pobierania danych użytkowników: {e}"}]

    context = {
        'weather': weather_data,
        'chart_uri': chart_uri,
        'users_stats': users_stats
    }

    return render(request, 'external_data/dashboard.html', context)


def weather_summary_api(request):

    try:
        lat, lon = 54.5189, 18.5305
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&timezone=Europe%2FWarsaw"

        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        temps = data['hourly']['temperature_2m'][:24]

        summary = {
            'location': 'Gdynia',
            'forecast_hours': 24,
            'average_temp': round(sum(temps) / len(temps), 2),
            'min_temp': min(temps),
            'max_temp': max(temps)
        }
        return JsonResponse(summary)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
