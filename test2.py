import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2 as pdf

# Load the environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# Example usage
job_description = "Seeking a talented Software Engineer with a passion for innovation. Must have strong experience in Python, Java, and Machine Learning. 3+ years of experience required."

# Replace 'resume.pdf' with the actual path to the PDF file of the candidate's resume
candidate_resume_path = "Resume.pdf"

# Extract the resume text from the PDF
candidate_resume_text = input_pdf_text(candidate_resume_path)

# Generate the content using the model
response = model.generate_content([
    "System Instructions: Task: Predict a single match score between 0 and 100 for a given job description and candidate resume.",
    "Inputs: Job Description: A text-based input describing the job requirements. Candidate Resume: The candidate's qualifications and experience in text format.",
    f"Job Description: {job_description}",
    f"Candidate Resume: {candidate_resume_text}",
    "Output: The output should be a single, numerical value representing the match score. The value should be a decimal number between 0 and 100."
])

# Extract the numerical match score using regex
match_score_pattern = re.search(r"(\d{2,3})-(\d{2,3})", response.text)
if match_score_pattern:
    # Calculate the average of the range
    lower_bound = float(match_score_pattern.group(1))
    upper_bound = float(match_score_pattern.group(2))
    match_score = (lower_bound + upper_bound) / 2
else:
    match_score = None

# Print the match score if found
if match_score is not None:
    print(f"Match Score: {match_score}")
else:
    print("Match score not found in the response.")

print(response.text)