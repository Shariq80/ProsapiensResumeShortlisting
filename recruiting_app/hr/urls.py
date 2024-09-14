from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('add-job/', views.add_job_posting, name='add_job_posting'),
    path('job/<int:job_id>/', views.view_job_posting, name='view_job_posting'),
]
