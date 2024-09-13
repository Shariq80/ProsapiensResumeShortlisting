from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Application, CandidateProfile
from .forms import ApplicationForm, CandidateProfileForm
from hr.models import JobPosting
from .utils import calculate_match_score

def job_list(request):
    jobs = JobPosting.objects.all()
    return render(request, 'candidates/job_list.html', {'jobs': jobs})

@login_required
def create_candidate_profile(request):
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('job_list')  # Redirect to a page where the user can view available jobs
    else:
        form = CandidateProfileForm()
    return render(request, 'candidates/create_profile.html', {'form': form})

@login_required
def apply_for_job(request, job_id):
    job = JobPosting.objects.get(id=job_id)
    try:
        candidate_profile = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return redirect('profile_creation')  # Redirect to a page where the user can create a profile

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = candidate_profile
            application.job_posting = job
            application.save()

            # Calculate match score
            match_score = calculate_match_score(job.description, application.resume.path)
            application.match_score = match_score
            application.save()

            return redirect('application_success')
    else:
        form = ApplicationForm()
    return render(request, 'candidates/apply.html', {'form': form, 'job': job})

def application_success(request):
    return render(request, 'candidates/application_success.html')
