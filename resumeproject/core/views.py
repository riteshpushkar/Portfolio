from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *
from django.http import HttpResponse

def convert_to_ist(timestamp):
    # Convert the UNIX timestamp to a datetime object
    utc_time = datetime.utcfromtimestamp(timestamp)
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    return ist_time.strftime('%H:%M')
def home(request):

    
    # x---x---x---x---x---x---x---  weather start   ---x---x---x---x---x---x---x---x

    payload = {}

    city = request.GET.get('city', 'Mumbai')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=53529b9c98d61da45cb30d365763d0c6'

    try:
        # Request to OpenWeatherMap API
        response = requests.get(url)
        
        # Successful request (status code 200)
        if response.status_code == 200:
            # Parsing the JSON response
            data = response.json()
            # Construct payload dictionary with relevant data
            payload = {'city': data['name'], 
                       'temperature': int(data['main']['temp'] - 273),
                       'pressure': data['main']['pressure'],
                       'humidity': data['main']['humidity'],
                       'weather': data['weather'][0]['main'],
                      }
            sunrise = convert_to_ist(data['sys']['sunrise'])
            sunset = convert_to_ist(data['sys']['sunset'])
            payload['sunrise'] = sunrise
            payload['sunset'] = sunset
            # print(payload)
        else:
            # If the request was not successful, print an error message
            print("Failed to fetch weather data. Status code:", response.status_code)
    except requests.RequestException as e:
        # If an error occurs during the request (e.g., network issues), print the error
        print("An error occurred during the request:", e)

    #---x---x---x---x---x---x--- weather finish  ---x---x---x---x---x---x---x---x
            

    # ---x---x---x---x---x---x---x---  clock and calander start  ---x---x---x---x---x---x---x---x---x

    now = datetime.now()
    hr = now.strftime("%H")
    min = now.strftime("%M %p")
    date = now.strftime("%d-%m-%Y")
    month = now.strftime("%m")
    year = now.strftime("%Y")
    year = int(year)
    month = int(month)
    hr = str(int(hr) % 12)
    time =  hr + ":" + min+ " IST"

    mon = request.GET.get('month')
    yr = request.GET.get('year')

    try:
        if mon:
            month = int(mon)
        if yr:
            year = int(yr)
        cal = HTMLCalendar().formatmonth(year, month)
    except Exception as e:
        cal = ''
        print(f'Error generating calendar: {mon} month and {yr}')

    context = {'date': date, 
               'time': time, 
               'month': month, 
               'year': year, 
               'cal': cal,
               'home': 'active'
              }

    context.update(payload)
    
    return render(request, 'core/home.html', context)

    # ---x---x---x---x---x---   clock and calander ends   ---x---x---x---x---x---x---x---x---x

from django.shortcuts import render, HttpResponse
from .models import Contact  # Import your Contact model if not imported already

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        description = request.POST.get('message')
        
        Contact.objects.create(name=name, email=email, subject=subject, message=description)

        response_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Contact Form Response</title>
                <style>
                    body {{
                        background-color: #000;
                        color: #fff;
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        text-align: center;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 100px auto;
                        padding: 20px;
                        border-radius: 10px;
                        background-color: #333;
                    }}
                    ul {{
                        list-style-type: none;
                        padding: 0;
                    }}
                    li {{
                        margin-bottom: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Your message has been saved successfully!</h1>
                    <p>Your message with the following details:</p>
                    <ul>
                        <li>Name: {name}</li>
                        <li>Email: {email}</li>
                        <li>Subject: {subject}</li>
                        <li>Description: {description}</li>
                    </ul>
                    <p>has been saved successfully in the database.</p>
                    <p>For quick reply, please use email/LinkedIn, as your message might be lost or not checked.</p>
                </div>
            </body>
            </html>
        """

        return HttpResponse(response_html)

    context = {'contact': 'active'}
    return render(request, 'core/contact.html', context)

