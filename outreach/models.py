from django.db import models

class Speaker(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="speakers")

    def __str__(self):
        return self.name
    
class Opportunity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="opportunities", blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title