from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('apply/<int:pk>/', views.application_form, name='application_form'),
    path('hr/dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('hr/job/<int:pk>/applicants/', views.applicant_list, name='applicant_list'),
    path('accounts/signup/', views.signup, name='signup'),
]
