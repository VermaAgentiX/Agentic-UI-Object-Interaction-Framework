
import requests
import os
import uuid

api_key = 'sk-VkhPTbhYBEqgqR1fzCNJ3E-Roz3VooZZfVCVUHObsV8'
url = "http://localhost:7860/api/v1/run/17830c3b-0124-438c-b9ec-86f2aa2e9c77"
  
# The complete API endpoint URL for this flow

 # The complete API endpoint URL for this flow

# Request payload configuration
payload = {
    "output_type": "chat",
    "input_type": "chat",
    "input_value": input('Type = ')
}
payload["session_id"] = str(uuid.uuid4())

headers = {"x-api-key": api_key}

try:
    # Send API request
    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception for bad status codes

    # Print response
    #print(response.text)  #Full ChatModel Output

    print('-----------------------xxx----------------------')
    data = response.json()

    answer = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]

    print(answer)

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
except ValueError as e:
    print(f"Error parsing response: {e}")