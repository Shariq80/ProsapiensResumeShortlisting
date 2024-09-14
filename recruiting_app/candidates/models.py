from django.db import models
from django.contrib.auth.models import User
from hr.models import JobPosting
from django.utils import timezone

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='candidate_applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    match_score = models.FloatField(default=0.0)
    applied_at = models.DateTimeField(auto_now_add=True)  # Switch to auto_now_add=True
