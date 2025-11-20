from djongo import models


class UserInfo(models.Model):
    # From Retell post-call analysis
    _id = models.ObjectIdField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)

    industry_type = models.CharField(max_length=100, null=True, blank=True)
    monthly_call_volume = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    primary_pain_point = models.CharField(max_length=255, null=True, blank=True)

    # New from your Retell fields
    appointment_time = models.DateTimeField(null=True, blank=True)
    their_problem = models.TextField(null=True, blank=True)

    # Call + raw payload
    call_id = models.CharField(max_length=255, unique=True)
    raw_payload = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'userInfo'

    def __str__(self):
        return f"{self.first_name or 'Unknown'} ({self.call_id})"
