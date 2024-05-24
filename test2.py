import requests

# Replace with your actual API key
API_KEY = "AIzaSyCgYYQCbZI7ALaJjUDn41ikrUz7PYG6188"

# Construct the correct API URL with HTTPS scheme
base_url = "https://api.bard.ai/v1/"

# Endpoint for text generation
text_generation_endpoint = "text"
translation_endpoint = "translate"
question_answering_endpoint = "question-answering"

def test_text_generation(prompt):
  """Sends a text generation request to Bard"""
  url = base_url + text_generation_endpoint
  headers = {"Authorization": f"Bearer {API_KEY}"}
  data = {"prompt": prompt}
  response = requests.post(url, headers=headers, json=data)
  response.raise_for_status()  # Raise exception for unsuccessful requests (>= 400)
  return response.json()["text"]

def test_translation(text, target_language):
  """Sends a translation request to Bard"""
  url = base_url + translation_endpoint
  headers = {"Authorization": f"Bearer {API_KEY}"}
  data = {"text": text, "target_language": target_language}
  response = requests.post(url, headers=headers, json=data)
  response.raise_for_status()
  return response.json()["translation"]

def test_question_answering(question):
  """Sends a question answering request to Bard"""
  url = base_url + question_answering_endpoint
  headers = {"Authorization": f"Bearer {API_KEY}"}
  data = {"question": question}
  response = requests.post(url, headers=headers, json=data)
  response.raise_for_status()
  return response.json()["answer"]

# Example usage
prompt = "Viết một bài thơ về mùa thu"
translated_text = test_translation("Hello, world!", "fr")
answer = test_question_answering("What is the meaning of life?")
generated_text = test_text_generation(prompt)

print(f"Generated text: {generated_text}")
print(f"Translated text: {translated_text}")
print(f"Answer to question: {answer}")
