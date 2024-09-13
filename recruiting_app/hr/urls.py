from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_job_posting, name='create_job_posting'),
    path('list/', views.job_list, name='job_list'),
    path('applications/<int:job_id>/', views.view_applications, name='view_applications'),
]
