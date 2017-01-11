from  __future__ import absolute_import
from celery import task
from celery import shared_task
from interface.models import celeryResponse


@shared_task
def analysis(message):
    # writes a message to the database
    logged_analysis = celeryResponse(output = message)
    logged_analysis.save()
    print message
    # saving to database
