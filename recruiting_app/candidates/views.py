from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application, CandidateProfile
from .forms import ApplicationForm
from hr.models import JobPosting
from .utils import calculate_match_score


def job_list(request):
    jobs = JobPosting.objects.all()
    return render(request, 'candidates/job_list.html', {'jobs': jobs})

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    
    # Ensure that CandidateProfile exists or create one if not
    candidate_profile, created = CandidateProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = candidate_profile  # Use the candidate profile
            application.job_posting = job
            application.save()

            # Calculate match score using resume
            match_score = calculate_match_score(job.description, application.resume.path)
            application.match_score = match_score
            application.save()

            return redirect('application_success')
    else:
        form = ApplicationForm()

    return render(request, 'candidates/apply.html', {'form': form, 'job': job})
def application_success(request):
    return render(request, 'candidates/application_success.html')
