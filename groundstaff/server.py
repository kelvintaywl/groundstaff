import logging
import os

import falcon

from .libs.airtable import AirTable


TOKEN = os.getenv('AIRTABLE_TOKEN')
USER = os.getenv('AIRTABLE_USER')
BASE = os.getenv('AIRTABLE_BASE')
client = AirTable(USER, TOKEN)


class Reservation:
    def on_get(self, req, resp):
        resp.media = client.list(BASE)
    
    def on_put(self, req, resp):
        formula = "{earliest reservable} >= NOW()"
        reservations = client.list(BASE, filterByFormula=formula)
        print(reservations)
        # TODO: insert reservations to queue
        for r in reservations:
            client.update(BASE, r['id'], { 'status': 'queued' })
        resp.status_code = 204


api = falcon.API()
api.add_route('/reservation', Reservation())
