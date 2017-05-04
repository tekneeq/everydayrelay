from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from django.db import models
import numpy as np
import redis

class Wine(models.Model):
    name = models.CharField(max_length=200)

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)

    def __unicode__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    wine = models.ForeignKey(Wine)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)

class News(models.Model):
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Address(models.Model):
    addr = models.CharField(max_length=100, verbose_name="Type your email address")
    user_name = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

class RelayAddress(models.Model):
    user_email = models.ForeignKey(Address)
    relay_email = models.CharField(max_length=100, verbose_name="Type your email here...")
    user_name = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

class UserProfile(models.Model):  
    user = models.OneToOneField(User)
    email_limit = models.CharField(max_length=140)  
    relay_limit = models.CharField(max_length=140, default=2)  

    def __unicode__(self):
        return self.user.username

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
def get_redis_connection():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        u_p = instance.userprofile
        u_p.email_limit = 1
        u_p.relay_limit = 2
        u_p.save()

        default_credit = 100
        r = get_redis_connection()
        r.hset('ucredits', instance.username, default_credit)

post_save.connect(create_user_profile, sender=User)

