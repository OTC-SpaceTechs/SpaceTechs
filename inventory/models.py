from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    custodian = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True, blank=True, related_name="equipment_custodian")
    checked_out_to_project = models.ForeignKey("projects.Project", on_delete=models.SET_NULL, null=True, blank=True, related_name="equipment_checked_out")
    approved_by = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True, blank=True, related_name="equipment_approved_by")

    def __str__(self):
        return f"{self.name} - {self.quantity} x {self.supplier}"