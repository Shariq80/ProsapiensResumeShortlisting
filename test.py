import os
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
    system_instruction="Predict a match score between 0 and 100 for a given job description and candidate resume. The output should be a single, numerical value representing the match score. The value should be a decimal number between 0 and 100.",
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
candidate_resume_path = "Resume - Ahmed Ashfaq.pdf"

# Extract the resume text from the PDF
candidate_resume_text = input_pdf_text(candidate_resume_path)

# Generate the content using the model
response = model.generate_content([
    "System Instructions: Task: Predict a match score between 0 and 100 for a given job description and candidate resume.",
    "Inputs: Job Description: A text-based input describing the job requirements. Candidate Resume: The candidate's qualifications and experience in text format.",
    f"Job Description: {job_description}",
    f"Candidate Resume: {candidate_resume_text}",
    "Output: The output should be a single, numerical value representing the match score. The value should be a decimal number between 0 and 100."
])

# Print the model's response
print(response.text)