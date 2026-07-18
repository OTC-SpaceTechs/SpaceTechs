from django.db import models
from django.utils import timezone


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


class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=300, blank=True)
    body = models.TextField(help_text='Markdown supported. Upload photos below and paste the snippet where you want them to appear. Add {: width="300" } right after an image to resize it, e.g. ![caption](url){: width="300" }.')
    image = models.ImageField(blank=True, null=True, upload_to='articles/covers/', help_text="Cover photo shown on cards and at the top of the article.")
    author = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to='articles/photos/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return self.caption or f"Photo for {self.article.title}"

    def markdown_snippet(self):
        return f"![{self.caption}]({self.image.url})"
