from django.contrib import admin
from .models import User, Notification, Emergency, Notifications
# Register your models here.

admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Notifications)

admin.site.register(Emergency)