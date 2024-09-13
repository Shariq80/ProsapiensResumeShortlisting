from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('create-profile/', views.create_candidate_profile, name='create_candidate_profile'),
    path('application-success/', views.application_success, name='application_success'),
]
