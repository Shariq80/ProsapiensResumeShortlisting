import os
import re
import google.generativeai as genai
import PyPDF2 as pdf

# Load environment variables for API key
GENIUS_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Generative AI API
genai.configure(api_key=GENIUS_API_KEY)

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
    """
    Extracts text from a PDF resume file.
    
    :param pdf_file_path: The file path of the uploaded resume PDF.
    :return: Extracted text as a string.
    """
    reader = pdf.PdfReader(pdf_file_path)
    resume_text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        resume_text += page.extract_text()
    return resume_text

# Function to generate the match score using Google Gemini API
def generate_match_score(job_description, resume_text):
    """
    Predicts a match score between a job description and resume using the Gemini API.
    
    :param job_description: The job description text.
    :param resume_text: The candidate resume text.
    :return: The calculated match score (float) or None if not found.
    """
    # Prepare the prompt for the API request
    prompt = [
        "System Instructions: Task: Predict a single match score between 0 and 100 for a given job description and candidate resume.",
        "Inputs: Job Description: A text-based input describing the job requirements. Candidate Resume: The candidate's qualifications and experience in text format.",
        f"Job Description: {job_description}",
        f"Candidate Resume: {resume_text}",
        "Output: The output should be a single, numerical value representing the match score. The value should be a decimal number between 0 and 100."
    ]
    
    # Generate the response from the model
    response = model.generate_content(prompt)
    
    # Use regex to extract the numerical match score
    match_score_pattern = re.search(r"(\d{2,3})-(\d{2,3})", response.text)
    
    if match_score_pattern:
        lower_bound = float(match_score_pattern.group(1))
        upper_bound = float(match_score_pattern.group(2))
        match_score = (lower_bound + upper_bound) / 2
    else:
        match_score = None

    return match_score

# Example usage (for testing purposes)
if __name__ == "__main__":
    job_description = "Seeking a talented Software Engineer with a passion for innovation. Must have strong experience in Python, Java, and Machine Learning. 3+ years of experience required."
    resume_file_path = "Resume.pdf"  # Replace with actual file path
    
    # Extract resume text from PDF
    candidate_resume_text = extract_resume_text(resume_file_path)
    
    # Generate the match score
    match_score = generate_match_score(job_description, candidate_resume_text)
    
    # Output the match score
    if match_score is not None:
        print(f"Match Score: {match_score}")
    else:
        print("Match score not found in the response.")
