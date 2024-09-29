from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class User(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)
#     cash = models.IntegerField()
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"


class Floor(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"{self.number} Поверх"


class Room(models.Model):
    number = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    describe = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.floor} - {self.number} кімната"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booking')

    def __str__(self):
        return f"{self.user.username} - {self.room}"

