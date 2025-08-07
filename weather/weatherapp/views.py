from django.shortcuts import render
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
def get_city_from_ip(request):
    get_user_ip(request)  # Log user IP address
    ip_api_url= f'http://ip-api.com/json/{get_user_ip(request)}'
    try:
        response = requests.get(ip_api_url)
        data = response.json()
        if data['status'] == 'success':
            return data['city']
        else:
            return 'Dhaka'  # Default city if IP lookup fails
    except requests.RequestException as e:
        print("IP API error:", e)
        return 'Dhaka'    
    

def Home(request):
    city = get_city_from_ip(request)  # Get city from IP address
    description = icon = temp = image_url = ''
    exception_occurred = False
    params = {'units': 'metric'}

    if request.method == 'POST':
        city = request.POST.get('city', 'Dhaka')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code != 200 or 'weather' not in data:
                exception_occurred = True
            else:
                description = data['weather'][0]['description']
                icon = data['weather'][0]['icon']
                temp = round(data['main']['temp'])
                image_url = select_image_based_on_weather(description, icon)
                

        except Exception as e:
            print("API error:", e)
            exception_occurred = True


    else:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
        response = requests.get(url, params=params)
        data = response.json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = round(data['main']['temp'])
        image_url = select_image_based_on_weather(description, icon)

    return render(request, 'home.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': datetime.date.today(),
        'city': city,
        'exception_occurred': exception_occurred,
        'image_url': image_url,
    })



def select_image_based_on_weather(description, icon):
    desc = description.lower()
    is_night = icon.endswith('n')  # True if night

    if 'thunderstorm' in desc:
        return 'https://images.pexels.com/photos/1118863/pexels-photo-1118863.jpeg'

    elif 'drizzle' in desc:
        return 'https://images.pexels.com/photos/1565572/pexels-photo-1565572.jpeg'

    elif 'rain' in desc:
        return 'https://images.pexels.com/photos/110874/pexels-photo-110874.jpeg' if not is_night else 'https://images.pexels.com/photos/1559799/pexels-photo-1559799.jpeg'

    elif 'snow' in desc:
        return 'https://images.pexels.com/photos/2896490/pexels-photo-2896490.jpeg' if not is_night else 'https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg'

    elif 'mist' in desc or 'fog' in desc or 'haze' in desc:
        return 'https://images.pexels.com/photos/226919/pexels-photo-226919.jpeg'

    elif 'smoke' in desc:
        return 'https://images.pexels.com/photos/569993/pexels-photo-569993.jpeg'

    elif 'dust' in desc or 'sand' in desc or 'ash' in desc:
        return 'https://images.pexels.com/photos/248159/pexels-photo-248159.jpeg'

    elif 'squall' in desc or 'tornado' in desc:
        return 'https://images.pexels.com/photos/1446076/pexels-photo-1446076.jpeg'

    elif 'cloud' in desc:
        return 'https://images.pexels.com/photos/158163/clouds-cloudporn-weather-lookup-158163.jpeg' if not is_night else 'https://images.pexels.com/photos/210186/pexels-photo-210186.jpeg'

    elif 'clear' in desc:
        return 'https://images.pexels.com/photos/414659/pexels-photo-414659.jpeg' if not is_night else 'https://images.pexels.com/photos/355465/pexels-photo-355465.jpeg'

    else:
        return 'https://images.pexels.com/photos/531756/pexels-photo-531756.jpeg'


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    
    return ip

