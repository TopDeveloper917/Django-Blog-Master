import requests
from django.contrib.auth.models import User
import pytz
from datetime import datetime
import logging


def enrich_data(user_id, ip):
    try:
        user_queryset = User.objects.filter(id=user_id)
        if user_queryset.exists():
            user = user_queryset.first()
            user = User.objects.get(id=user_id)
            print(ip)
            ip_geolocation_response = requests.get(f'https://ipgeolocation.abstractapi.com/v1/?api_key=1684f0235d154e2b8439fe831f9a1cdc&ip_address={ip}')
            ip_geolocation_data = ip_geolocation_response.json()
            print(ip_geolocation_data)
            user_country_code = ip_geolocation_data.get('country_code')
            user_timezone = ip_geolocation_data.get('timezone').get('name')
            user.userprofile.location = ip_geolocation_data.get('city')
            user.userprofile.ip_address = ip
            timezone = pytz.timezone(user_timezone)
            today = datetime.now(timezone)
            user.userprofile.date = today.strftime('%Y-%m-%d')
            holiday_response = requests.get(f'https://holidays.abstractapi.com/v1/?api_key=ae814c2088b747d18f38959bd95ea28e&country={user_country_code}&{today.year}&month={today.month}&day={today.day}')
            holidays_data = holiday_response.json()
            if holidays_data[0].type == 'National':
                user.userprofile.is_holiday = True
            else:
                user.userprofile.is_holiday = False
            user.userprofile.save()
    except Exception as e:
        print('')
