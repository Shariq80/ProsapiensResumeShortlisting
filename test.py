import google.generativeai as genai
import os

# Set API key directly for testing
api_key = "AIzaSyDkjb7xJnoTsUXeQlzUf6kh7-fkogtEps0"
genai.configure(api_key=api_key)

# Test request
def test_api():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    print(response.text)

test_api()
