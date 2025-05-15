from django.db import models


class Appointment(models.Model):
    place = models.TextField(default='London')
    initiator = models.CharField(max_length=100)
    guest = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.initiator} {self.date}"
