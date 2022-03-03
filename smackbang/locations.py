import numpy as np
import pandas as pd
import requests

def get_city_location(cities):
    city_url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/cities.json"
    headers = {
        'x-access-token': "ccf49e56bc37cdcbea0545a0a08b7e08",
        'x-rapidapi-host': "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
        'x-rapidapi-key': "062d5d04d0msh9bf753a499a46f8p1d18edjsn469f78c5d3ac"
    }

    response = requests.request("GET", city_url, headers=headers).json()

    city_location = []

    for city in cities:
        df = pd.DataFrame.from_dict(response)[['code', 'coordinates']].dropna()
        city_location.append(df.loc[df['code'] == city].coordinates.apply(pd.Series))
    result = pd.concat(city_location)
    df = pd.DataFrame(cities)

    result["city_code"] = df.values
    result.reset_index(inplace = True)
    result.drop(columns="index", inplace =True)
    return result
