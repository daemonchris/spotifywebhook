from django.db import models


"""
add the user from
user_id: Int,
timestamp: datetime,
songs: [
{title: String,
artist: String,
genre: String,
album: String,
date_released, datetime,
playlist: String (nullable),
total_streams: Int (this is the number of times this user has streamed),
global_streams: Int,
us_streams: Int }
]}
"""
from django.db import models
from django.utils import timezone

from django_hstore import hstore


class WebhookTransaction(models.Model):
    UNPROCESSED = 1
    PROCESSED = 2
    ERROR = 3

    STATUSES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    date_generated = models.DateTimeField()
    date_received = models.DateTimeField(default=timezone.now)
    body = hstore.SerializedDictionaryField()
    request_meta = hstore.SerializedDictionaryField()
    status = models.CharField(max_length=250, choices=STATUSES, default=UNPROCESSED)

    objects = hstore.HStoreManager()

    def __unicode__(self):
        return f'{self.date_event_generated}'


class Spotstream(models.Model):
    songs = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    date_released = models.DateTimeField()
