import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve your Spotify credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Spotify Authentication URL for Client Credentials Flow
AUTH_URL = "https://accounts.spotify.com/api/token"

def get_spotify_token():
    """
    Obtain an access token from Spotify using Client Credentials Flow.
    """
    auth_response = requests.post(AUTH_URL, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    
    auth_response_data = auth_response.json()
    
    # Return the access token from the response
    return auth_response_data.get("access_token")

def search_track(query, limit=5):
    """
    Search for a track on Spotify.
    
    Parameters:
      query (str): The search string (song or artist).
      limit (int): Number of items to return.
      
    Returns:
      dict: JSON response from Spotify with search results.
    """
    token = get_spotify_token()
    if not token:
        return {"error": "Could not get Spotify token."}
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    search_url = "https://api.spotify.com/v1/search"
    params = {
        "q": query,
        "type": "track",
        "limit": limit
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    return response.json()

# For testing purposes only
if __name__ == "__main__":
    query = input("Enter a song or artist to search: ")
    results = search_track(query)
    print(results)
