from django.db import models
from django.contrib.auth.models import User


class Floor(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"{self.number} Поверх"


class Room(models.Model):
    number = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    describe = models.TextField()
    photo = models.ImageField(upload_to="static/images/")
    rating = models.FloatField(default=0.0)
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    classes = models.CharField(max_length=9, choices=[
        ('_economy', 'Економ'), ('_comfort', 'Комфорт'), ('_business', "Бізнес"), ('_premium', 'Преміум')
    ])

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            avg_rating = round(avg_rating, 1)
            self.rating = avg_rating if avg_rating else 0.0
        else:
            self.rating = 0.0
        self.save()

    def __str__(self):
        return f"{self.floor} - {self.number} кімната {self.price} UAH"


class Review(models.Model):
    room = models.ForeignKey(Room, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.room.update_rating()

    def delete(self, *args, **kwargs):
        room = self.room
        super().delete(*args, **kwargs)
        room.update_rating()


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    start_time = models.DateField()
    end_time = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booking')

    status = models.CharField(max_length=8, choices=[
        ('_waiting', 'Waiting'),
        ("_active", "Active"),
        ("_done", "Done")
    ])

    def __str__(self):
        return f"{self.user.username} - {self.room}"
