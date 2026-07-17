from django.db import models


class Event(models.Model):
    class EventTypes(models.TextChoices):
        MEETING = "MEETING", "Meeting"
        SOCIAL = "SOCIAL", "Social"
        LAUNCH = "LAUNCH", "Launch"
        FUNDRAISER = "FUNDRAISER", "Fundraiser"
        WORKSHOP = "WORKSHOP", "Workshop"

    title = models.CharField(max_length=250)
    date = models.DateTimeField()
    event_type = models.CharField(max_length=26, choices=EventTypes.choices, default=EventTypes.MEETING)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} ({self.date:%Y-%m-%d})"
