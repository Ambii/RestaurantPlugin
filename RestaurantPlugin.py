from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import requests

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class PluginResponse(BaseModel):
    model: Dict[str, Any]
    messages: list[Message]

# You need a Google API key for the Places API.
# Replace 'your-api-key' with your actual key.
GOOGLE_API_KEY = 'AIzaSyAWGMRwdEBJwzImoZ4ez33nvsPWyCCpLBw'

@app.post("/v1/messages", response_model=PluginResponse)
async def receive_message(message: Message):
    # Assume the user message contains a location.
    location = message.content

    # Make a request to the Google Places API.
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': location,
        'radius': 500,  # search in a 500m radius
        'type': 'restaurant',
        'key': GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Compile the names of the restaurants into a single string.
    restaurant_names = [result['name'] for result in data['results']]
    response_content = ', '.join(restaurant_names)

    response_message = Message(role="assistant", content=response_content)

    return PluginResponse(model={}, messages=[response_message])
