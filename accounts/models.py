from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('vendor', 'Vendor'),
        ('paramedic', 'Paramedic')
    )

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)
    facility_uid = models.CharField(max_length=12, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    photo = models.ImageField(upload_to='users', default='default.jpeg', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return f'{self.username}'

    class Meta:
    	ordering = ['-date_created']



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=30, null=True)
    end_time = models.CharField(max_length=30, null=True)
    max_heart_rate = models.FloatField(null=True)
    min_heart_rate = models.FloatField(null=True)
    avg_heart_rate = models.FloatField(null=True)
    calories = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='which_user')
    paramedic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='paramedic')
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.start_time} - {self.max_heart_rate}"


class Emergency(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True)
    #message = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='message', null=True)
    #messages = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    # Add additional fields as needed

    def __str__(self):
        return f"Emergency for {self.message} on {self.date_created}"



