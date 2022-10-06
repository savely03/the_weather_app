import requests
from django.shortcuts import render
from .models import City
from django.views import View
from .forms import CityForm
from django.http import HttpResponseRedirect


# Create your views here.

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?lang=ru&q={}&appid=ee51be248a056735e6c742f7d7c731ab'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            if requests.get(url.format(new_city)).ok:
                new_city_count = City.objects.filter(name__icontains=new_city).count()
                if new_city_count == 0:
                    form.save()
                else:
                    err_msg = 'City already exists in the database'
            else:
                err_msg = 'City does not exists in the world'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    weather_data = []

    cities = City.objects.all()
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': round(r['main']['temp'] - 273),
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']

        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather/weather.html', context=context)


class DeleteCityView(View):
    def get(self, request, city):
        city_delete = City.objects.get(name__icontains=city)
        city_delete.delete()
        return HttpResponseRedirect('/')
