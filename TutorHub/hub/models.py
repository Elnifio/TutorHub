from django.db import models

# This is the user model that contains all users that can log in to our website.
class User(models.Model):
    username = models.TextField();
    password = models.TextField();
    email = models.EmailField();
    is_admin = models.IntegerField(default=0);
    is_publisher = models.IntegerField(default=0);
    preference = models.TextField();
    pass


class Event(models.Model):
    name = models.TextField();
    date = models.DateTimeField(auto_now=True);
    description = models.TextField();
    pass

    
