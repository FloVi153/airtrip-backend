from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI()

# Deine Amadeus API-Daten
API_KEY = "qATAvnw2PALhXwNdmhaQ2EHFFtj8c4XM"
API_SECRET = "9H7cvvvuqPS0CKaD"

# Amadeus URLs
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

class FlightSearch(BaseModel):
    origin: str
    destination: str
    departureDate: str

def get_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': API_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Token Error")
    return response.json().get("access_token")

@app.post("/search-flights")
async def search_flights(flight: FlightSearch):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "originLocationCode": flight.origin.upper(),
        "destinationLocationCode": flight.destination.upper(),
        "departureDate": flight.departureDate,
        "adults": 1,
        "max": 5
    }
    response = requests.get(FLIGHT_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Flugabfrage fehlgeschlagen")
    return response.json()
