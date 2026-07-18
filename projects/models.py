from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE","Active"
        ARCHIVED = "ARCHIVED","Archived"
        PENDING = "PENDING", "Pending"

    status = models.CharField(max_length=20, choices=Status.choices)
    start_date = models.DateField(blank = True, null = True)

class ProjectContent(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="%(class)ss")
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Document(ProjectContent):
    file = models.FileField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class DocType(models.TextChoices):
        DESIGN = "DES", "Design"
        RESEARCH = "RES", "Research"
        PROCEDURE = "PROC", "Procedure"
        RESULTS = "RSLT", "Results"

    doc_type = models.CharField(max_length=4, choices=DocType.choices)

class Tip(ProjectContent):
    question = models.CharField(max_length=255)  # overrides/duplicates title's role slightly — see note below
    short_answer = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

class Component(models.Model):
    project = models.ForeignKey("Project", related_name='components')
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=255)
    notes = models.TextField()

