# from django.db import models

# class UserInfo(models.Model):
#     name = models.CharField(max_length=255)
#     age = models.IntegerField(null=True, blank=True)
#     gender = models.CharField(max_length=50, null=True, blank=True)
#     call_id = models.CharField(max_length=255, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']
#         db_table = 'UserInfo'

#     def __str__(self):
#         return f"{self.name} ({self.call_id})"



from djongo import models

class UserInfo(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    business_name = models.CharField(max_length=255, null=True, blank=True)

    industry_type = models.CharField(max_length=100, null=True, blank=True)
    monthly_call_volume = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    primary_pain_point = models.CharField(max_length=255, null=True, blank=True)
    time_preference = models.CharField(max_length=100, null=True, blank=True)

    intent = models.CharField(max_length=50, null=True, blank=True)
    lead_ready = models.BooleanField(null=True, blank=True)
    pain_intensity = models.CharField(max_length=50, null=True, blank=True)

    call_id = models.CharField(max_length=255, unique=True)
    raw_payload = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'userInfo'

    def __str__(self):
        return f"{self.first_name or 'Unknown'} ({self.call_id})"
