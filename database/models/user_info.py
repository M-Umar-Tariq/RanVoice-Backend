from django.db import models


class UserInfo(models.Model):
    call_id = models.CharField(max_length=255, unique=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    company_email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    industry_type = models.CharField(max_length=255, null=True, blank=True)

    transcript = models.TextField(null=True, blank=True)

    raw_payload = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} ({self.call_id})"

    class Meta:
        ordering = ['-created_at']
        db_table = 'userInfo'
