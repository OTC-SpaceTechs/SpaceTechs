from django.db import models

class Member(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add = True)
    active_status = models.BooleanField(default=True)
    major = models.TextField(blank = True, null = True)
    bio = models.TextField(blank = True, null = True)

class OfficerHistory(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    role = models.ForeignKey("auth.Group", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null = True, blank = True)