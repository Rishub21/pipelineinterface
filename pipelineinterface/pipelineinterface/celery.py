from __future__ import absolute_import, unicode_literals
import os
from celery import current_app
from celery.bin import worker
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pipelineinterface.settings')
#django.setup()
app = Celery('pipelineinterface')

app.config_from_object('django.conf:settings') # project settings
#app.config.update( CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',)
#app.conf.update(CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) # looks for a tasks.py file in every single app, to see what celery needs to do


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':

    worker = worker.worker(app=app)

    options = {

    }

    worker.run(**options)
