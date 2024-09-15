from django.db import models

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    years_of_experience = models.PositiveIntegerField()
    education = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    match_score = models.FloatField(null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.name} - {self.job_posting.title}"