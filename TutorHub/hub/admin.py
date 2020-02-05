from django.contrib import admin
from hub.models import User, Event, Tag

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Tag)