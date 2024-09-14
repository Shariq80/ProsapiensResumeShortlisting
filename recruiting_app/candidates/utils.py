import requests

def calculate_match_score(job_description, resume_path):
    api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    api_key = "AIzaSyCTybUGM9Scd-89yupOk7o2cD8vzh6_2BY"
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(resume_path, 'rb') as resume_file:
        files = {'resume': resume_file}
        data = {'job_description': job_description}
        response = requests.post(api_url, headers=headers, data=data, files=files)

    if response.status_code == 200:
        return response.json().get('match_score', 0)
    return 0
