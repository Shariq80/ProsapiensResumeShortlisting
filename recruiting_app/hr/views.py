from django.shortcuts import render, redirect
from .models import JobPosting
from .forms import JobPostingForm

def create_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.created_by = request.user
            job_posting.save()
            return redirect('job_list')
    else:
        form = JobPostingForm()
    return render(request, 'hr/create_job.html', {'form': form})

def job_list(request):
    jobs = JobPosting.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'hr/job_list.html', {'jobs': jobs})

def view_applications(request, job_id):
    job = JobPosting.objects.get(id=job_id)
    applications = job.application_set.order_by('-match_score')
    return render(request, 'hr/view_applications.html', {'applications': applications})
