import openai
import google.generativeai as genai
genai.configure(api_key="AIzaSyB781IlY0ddAzwSYVVg6_GIwLqOkKl0Tj0")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("what is fruits?")# Specify the model
print(response)
