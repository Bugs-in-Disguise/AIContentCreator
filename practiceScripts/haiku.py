from google import genai

client = genai.Client(api_key="AIzaSyC4_Of0KLBwuZ-x6JmzBroOnso580FnQCg")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Write a haiku"
)
print(response.text)
