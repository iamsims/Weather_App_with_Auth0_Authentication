import json, requests 
from django.core.cache import cache

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

with open('./cities.json', 'r') as f:
    my_json_obj = json.load(f)
    list_country_codes = list(map(lambda a:a['CityCode'], my_json_obj['List']))


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    print("Request session from callback", request.session)
    return redirect(request.build_absolute_uri(reverse("index")))

def logout(request):
    request.session.clear()
    print("Request session", request.session)

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def get_weather_data():
    list_country_codes_str= ",".join(list_country_codes)
    url = 'https://api.openweathermap.org/data/2.5/group?id={}&units=metric&appid=7d3a9f6a41a7d0e119afb759febfaea7'.format(list_country_codes_str)
    response = requests.get(url).json() #request the API data and convert the JSON to Python data types
    weather_data =[]
    # print(response)
    for city_response in response["list"]:
        weather = {
            "name":city_response["name"],
            "id":city_response["id"],
            "temp":city_response["main"]["temp"],
            "description":city_response["weather"][0]["description"]
        }
        weather_data.append(weather)


    return weather_data


def index(request):
    weather_data = cache.get('weathers')
    if weather_data is None:
        weather_data = get_weather_data()
        cache.set('weathers', weather_data, 2)

    context = {
    "weather_data": weather_data,
    "session": request.session.get("user")
    }

    return render(request, 'index.html', context) 