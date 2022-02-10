from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)


class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    note = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date')

