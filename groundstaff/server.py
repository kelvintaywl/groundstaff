import logging
import os

import falcon

from .libs.airtable import AirTable
from .libs.scheduler import get_scheduler
from .libs.time import (
    datetime_from_jst_date_string,
    datetime_from_iso8601,
    to_jst,
)

TOKEN = os.getenv('AIRTABLE_TOKEN')
USER = os.getenv('AIRTABLE_USER')
BASE = os.getenv('AIRTABLE_BASE')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')


client = AirTable(USER, TOKEN)
scheduler = get_scheduler(
    redis_host,
    redis_port,
    password=redis_password
)
scheduler.start()

def reserve(date, timeslot, is_indoor):
    # TODO: run selenium task
    print('hello')

def parse_fields(reservation):
    fields = reservation['fields']

    requested = fields['requested']
    duration = fields['duration']  # secs
    duration_hr = duration / (60 * 60)

    date_jst = to_jst(datetime_from_iso8601(requested))
    date = str(date_jst.date())  # yyyy-mm-dd
    # e.g., 1000, 1200 when duration_hr is 2
    timeslot = (date_jst.hour * 100, (date_jst.hour + duration_hr) * 100)
    is_indoor = fields['court'] == 'indoor'

    return date, timeslot, is_indoor

def setup_future_reservation(reservation, run_datetime):
    # use scheduler to set up future task of reserving
    

    args = parse_fields(res)
    scheduler.add_job(reserve, trigger='date', run_date=run_datetime, args=())


class Index:
    def on_get(self, req, resp):
        resp.media = 'curl -X GET /reservation'


class Reservation:
    def on_get(self, req, resp):
        resp.media = client.list(BASE)
    
    def on_put(self, req, resp):
        # filter where earliest reservable has not happened
        # and reservation has only been created (not queued, nor finished)
        formula = "AND({earliest reservable} >= NOW(), {status} = 'created')"
        reservations = client.list(BASE, filterByFormula=formula)
        for r in reservations:
            dt = r['fields']['earliest reservable']  # JST
            run_datetime = datetime_from_jst_date_string(dt)
            print(run_datetime)
            print(type(run_datetime))
            setup_future_reservation(r, run_datetime)
            client.update(BASE, r['id'], { 'status': 'queued' })
        resp.status_code = 204

class Schedule:
    def on_get(self, req, resp):
        resp.media = scheduler.get_jobs()

api = falcon.API()
api.add_route('/', Index())
api.add_route('/reservation', Reservation())
api.add_route('/schedule', Schedule())
