from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import JobPosting, Application
from .forms import ApplicationForm
from django.contrib.auth.forms import UserCreationForm
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2 as pdf
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import JobPosting, Application

load_dotenv()

def home(request):
    job_postings = JobPosting.objects.all()
    return render(request, 'core/home.html', {'job_postings': job_postings})

def job_detail(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    return render(request, 'core/job_detail.html', {'job_posting': job_posting})

def application_form(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_posting = job_posting
            application.save()
            return render(request, 'core/application_success.html')
    else:
        form = ApplicationForm()
    return render(request, 'core/application_form.html', {'form': form, 'job_posting': job_posting})

@login_required
def hr_dashboard(request):
    job_postings = JobPosting.objects.all()
    return render(request, 'core/hr_dashboard.html', {'job_postings': job_postings})

@login_required
def applicant_list(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    applications = Application.objects.filter(job_posting=job_posting).order_by('-created_at')
    return render(request, 'core/applicant_list.html', {'job_posting': job_posting, 'applications': applications})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


# Configure Google Generative AI API
def configure_genai():
    genai.configure(api_key="AIzaSyDkjb7xJnoTsUXeQlzUf6kh7-fkogtEps0")

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define the GenerativeModel
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Predict a single, numerical match score between 0 and 100 for a given job description and candidate resume. The value should be a decimal number between 0 and 100.",
)

# Function to extract text from a PDF file
def extract_resume_text(pdf_file_path):
    reader = pdf.PdfReader(pdf_file_path)
    resume_text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        resume_text += page.extract_text()
    return resume_text

# Function to generate the match score using Google Gemini API
def generate_match_score(job_description, resume_text):
    prompt = [
        "System Instructions: Task: Predict a single match score between 0 and 100 for a given job description and candidate resume.",
        "Inputs: Job Description: A text-based input describing the job requirements. Candidate Resume: The candidate's qualifications and experience in text format.",
        f"Job Description: {job_description}",
        f"Candidate Resume: {resume_text}",
        "Output: The output should be a single, numerical value representing the match score. The value should be a decimal number between 0 and 100."
    ]
    
    response = model.generate_content(prompt)
    
    # Use regex to extract the numerical match score
    match_score_pattern = re.search(r"(\d+\.\d+|\d+)", response.text)
    
    if match_score_pattern:
        match_score = float(match_score_pattern.group())
    else:
        match_score = None

    return match_score

# View to list applicants and their match scores
def applicant_list(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    applications = Application.objects.filter(job_posting=job_posting).order_by('-created_at')
    
    # Generate match scores for each application
    for application in applications:
        resume_text = extract_resume_text(application.resume.path)
        match_score = generate_match_score(job_posting.description, resume_text)
        application.match_score = match_score
    
    return render(request, 'core/applicant_list.html', {'job_posting': job_posting, 'applications': applications})