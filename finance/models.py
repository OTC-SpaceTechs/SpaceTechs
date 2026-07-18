from django.db import models

class PurchaseRequest(models.Model):
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="purchase_requests", null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.TextField()
    requested_by = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_requests_made")
    approved_by = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True, blank=True, related_name="purchase_requests_approved")
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase Request by {self.requested_by} for {self.amount} - Status: {self.status}"