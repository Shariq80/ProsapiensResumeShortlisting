from django.db import models
from django.contrib.auth.models import User
from hr.models import JobPosting  # Import the JobPosting model


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Example field
    skills = models.CharField(max_length=255, blank=True)  # Example field

    def __str__(self):
        return self.user.username

class Application(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    match_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Application from {self.candidate.user.username} for {self.job_posting.title}"
