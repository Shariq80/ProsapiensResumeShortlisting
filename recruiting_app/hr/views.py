from django.shortcuts import render, redirect
from .models import JobPosting, Application
from .forms import JobPostingForm

def hr_dashboard(request):
    jobs = JobPosting.objects.all()
    return render(request, 'hr/dashboard.html', {'jobs': jobs})

def add_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_dashboard')
    else:
        form = JobPostingForm()
    return render(request, 'hr/add_job.html', {'form': form})

def view_job_posting(request, job_id):
    job = JobPosting.objects.get(id=job_id)
    shortlisted_candidates = Application.objects.filter(job=job).order_by('-match_score')
    return render(request, 'hr/view_job.html', {'job': job, 'candidates': shortlisted_candidates})
