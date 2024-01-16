import os
import geocoder
from dotenv import load_dotenv

load_dotenv('.env')
key = os.environ.get('GEONAMES_KEY')


def get_town(town: str, lang: str, max_rows: int):
    res = geocoder.geonames(town, key=key, lang=lang, maxRows=max_rows)
    if res.status_code == 200:
        towns = []
        for i in res:
            town = {'country': i.country, 'state': i.state, 'town': i.address}
            if town not in towns:
                towns.append(town)
        return towns
    return []
