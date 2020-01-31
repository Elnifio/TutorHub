from django.db import models
import json

# This is the user model that contains all users that can log in to our website.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.TextField();
    password = models.TextField();
    email = models.EmailField();
    is_admin = models.BooleanField(default=False);
    is_publisher = models.BooleanField(default=False);
    preference = models.TextField(default="{}");
    tags = models.TextField(default="{}");
    
    def get_tags(self):
        return json.loads(self.tags)
    
    pass


class Event(models.Model):
    name = models.TextField();
    date = models.DateTimeField(auto_now=True);
    description = models.TextField();
    pass

    
