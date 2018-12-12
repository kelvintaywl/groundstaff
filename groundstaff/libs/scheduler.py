from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore

def get_scheduler(host, port, password=None):
    """ Returns an APScheduler instance with Redis store """
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores={
        'default': RedisJobStore(host=host, port=port, password=password)
    })
    return scheduler
