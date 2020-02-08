from django.db import models
import json

def get_suffix(day):
    if day == "01" or day == "21" or day == "31":
        return "st"
    elif day == "02" or day == "22":
        return "nd"
    elif day == "03" or day == "23":
        return "rd"
    else:
        return "th"

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
    date = models.DateTimeField()
    description = models.TextField(default="")
    tags = models.TextField(default={})
    hoster = models.TextField(default="")
    location = models.TextField(default="")
    likes = models.IntegerField(default=0)
    poster = models.ImageField(upload_to='usr_img')

    def __str__(self):
        self.get_time()
        return self.name + " @ " + self.get_time() + " :: " + str(self.event_id)

    def get_time(self):
        time = self.date
        time = time.ctime().split(" ")
        # out = time[4] + ", "+ time[0] + ", " + time[1] + " " + time[3] + get_suffix(time[3].zfill(2))  + ", " + time[5]
        out = str(self.date)
        return out

    def get_name(self):
        return self.name.split(" ").join("_")
    
    def get_tags(self):
        return json.loads(self.tags)

    def like(self):
        self.likes += 1
        self.save()
    pass

    
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.TextField(default="")
    events = models.TextField(default="[]")

    def __str__(self):
        return str(self.tag_id) + " :: " + self.tag_name

    def register_event(self, event_id):
        events = json.loads(self.events)
        events.append(event_id)
        self.events = json.dumps(events)
        self.save()

    def get_all_related_events(self):
        events = json.loads(self.events)
        out = Event.objects.none()
        for item in events:
            out = out.union(Event.objects.filter(event_id=item))
        return out
    