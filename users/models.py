from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofiles', on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(null=True, blank=True, max_length=200)
    country = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        unique_together = ('user', 'full_name')

    def __str__(self):
        return 'user: %s; full_name: %s' % (self.user, self.full_name)
