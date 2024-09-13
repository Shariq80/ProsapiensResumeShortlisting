from django.db import models
from django.contrib.auth.models import User

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # HR employee who created the job posting
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
