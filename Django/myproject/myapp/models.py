from django.db import models

# Create your models here.
from django.db import models

class Issue(models.Model):
    STATUS_CHOICES = [
        ('INQUEUE', 'In Queue'),
        ('ASSIGNED', 'Assigned'),
        ('DISPATCHED', 'Dispatched'),
    ]

    issueID = models.AutoField(primary_key=True)
    userID = models.IntegerField()
    location = models.CharField(max_length=100)
    problem = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INQUEUE')
class Agents(models.Model):
    agentID = models.AutoField(primary_key=True)
    queue = models.IntegerField(default=0)
class Mechanic(models.Model):
    mechanicID = models.AutoField(primary_key=True)
    availability = models.BooleanField(default=True)

