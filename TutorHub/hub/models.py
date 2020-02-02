from django.db import models
import json

# This is the user model that contains all users that can log in to our website.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.TextField()
    password = models.TextField()
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    preference = models.TextField(default="[]")
    tags = models.TextField(default="[]")
    saved_events = models.TextField(default="[]")

    def get_tags(self):
        return json.loads(self.tags)
    
    pass


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.TextField()
    date = models.DateTimeField(auto_now=True)
    description = models.TextField(default="")
    tags = models.TextField(default={})
    hoster = models.TextField(default="")
    location = models.TextField(default="")
    likes = models.IntegerField(default=0)

    def get_name(self):
        return self.name.split(" ").join("_")
    
    def get_tags(self):
        return json.loads(self.tags)

    def like(self):
        self.likes += 1
        self.save()
    pass

    
