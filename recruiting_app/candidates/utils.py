# candidates/utils.py
import requests

def calculate_match_score(job_description, resume_pdf):
    api_url = "https://ai.google.com/v1/match-score"
    api_key = "AIzaSyCTybUGM9Scd-89yupOk7o2cD8vzh6_2BY"
    headers = {"Authorization": f"Bearer {api_key}"}

    data = {
        "job_description": job_description,
        "resume": resume_pdf
    }

    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('match_score', 0)
    return 0
