import logging
import os
from functools import partial

import requests


class SETTINGS:
    VERSION = 'v0'
    URL = 'https://api.airtable.com/{version}/{user}/{base}'
    GRID_VIEW = 'Grid view'
    MAX_ITEMS = 200
    USER_LOCALE = 'Asia/Tokyo'

class AirTable:

    def __init__(self, user, token):
        self.user = user
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
        }
        # self.url(base=base) to get full URL
        self.url = partial(
            SETTINGS.URL.format,
            version=SETTINGS.VERSION,
            user=user
        )
    
    def list(self, base, **kwargs):
        params = kwargs
        params.update(
            {
                'view': SETTINGS.GRID_VIEW,
                'userLocale': SETTINGS.USER_LOCALE
            }
        )
        response = requests.get(
            self.url(base=base),
            params,
            headers=self.headers
        )
        if response.status_code >= 400:
            logging.error('failed to fetch records for base', response.text)
        return response.json().get('records', [])
    
    def get(self, base, id):
        response = requests.get(
            f'{self.url(base=base)}/{id}',
            headers=self.headers
        )
        return response.json() 

    def update(self, base, id, data):
        response = requests.patch(
            f'{self.url(base=base)}/{id}',
            json={'fields': data },
            headers=self.headers,
        )
        if response.status_code >= 400:
            logging.error('failed to patch record for base', response.text)
        return response.json()
