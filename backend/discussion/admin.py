from django.contrib import admin
from .models import Topic, Comment

# Register your models here.
admin.site.register(Topic)
admin.site.register(Comment)