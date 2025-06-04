import openai
import google.generativeai as genai
genai.configure(api_key="Your API Key here")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("what is fruits?")# Specify the model
print(response)
