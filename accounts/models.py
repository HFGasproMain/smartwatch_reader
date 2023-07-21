from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('vendor', 'Vendor'),
        ('paramedic', 'Paramedic')
    )
    USER_HEALTH_CHOICES = (
        ('unknown', 'unknown'),
        ('stable', 'stable'),
        ('critical', 'critical'),
    )

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    hospital_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    email_address = models.EmailField(null=True)
    state = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=255, null=True)
    availability = models.BooleanField(default=True)
    facility_uid = models.CharField(max_length=12, null=True)
    smartwatch_serialno = models.CharField(max_length=12, null=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    health_status = models.CharField(max_length=50, choices=USER_HEALTH_CHOICES, default='unknown')
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


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=30, null=True)
    end_time = models.CharField(max_length=30, null=True)
    max_heart_rate = models.FloatField(null=True)
    min_heart_rate = models.FloatField(null=True)
    avg_heart_rate = models.FloatField(null=True)
    calories = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notified_user')
    paramedic = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='paramedics')
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} => {self.start_time} - {self.calories} - {self.max_heart_rate} - {self.min_heart_rate}"



class Emergency(models.Model):
    E_CHOICES = (
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    )
    notification = models.ForeignKey(Notifications, on_delete=models.CASCADE, null=True)
    paramedic = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='assigned_paramedic')
    issue = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=20, choices=E_CHOICES, default='pending')
    doc_message = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Emergency for {self.notification} on {self.date_created}"

    class Meta:
        ordering=('-date_created',)



