import requests
import json


def location(request):
    
    res = requests.get('http://ip-api.com/json/61.3.97.21')
    location_data = res.text
    data = json.loads(location_data)
    for key, value in data.items():
        print(key, value)
        if key == "city":
            print(value)
            break
    
   