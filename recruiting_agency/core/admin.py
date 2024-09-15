from django.contrib import admin
from .models import JobPosting, Application

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_posting', 'email', 'created_at')
