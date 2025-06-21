import requests
import base64
import os

# Load from environment or replace with your actual client ID and secret for testing
CLIENT_ID = os.getenv("CLIENT_ID", "your_client_id_here")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "your_client_secret_here")

AUTH_URL = 'https://accounts.spotify.com/api/token'
SEARCH_URL = 'https://api.spotify.com/v1/search'
RECOMMEND_URL = 'https://api.spotify.com/v1/recommendations'

def get_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(AUTH_URL, headers=headers, data=data)
    response.raise_for_status()
    token = response.json()["access_token"]
    return token

def search_track(query, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": "track",
        "limit": 10
    }

    response = requests.get(SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        print("❌ SEARCH FAILED:", response.status_code, response.text)
        return []

    results = response.json()
    tracks = []
    for item in results.get("tracks", {}).get("items", []):
        track = {
            "id": item["id"],
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "artist_id": item["artists"][0]["id"],
            "genre": "pop",  # Default genre
            "image": item["album"]["images"][0]["url"] if item["album"]["images"] else ""
        }
        tracks.append(track)

    return tracks

def get_recommendations(track_id, artist_id, genre, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "limit": 5,
        "seed_tracks": track_id,
        "seed_artists": artist_id,
        "seed_genres": genre
    }

    response = requests.get(RECOMMEND_URL, headers=headers, params=params)

    # Debug output
    print("📡 RECOMMEND REQUEST URL:", response.url)
    print("📡 STATUS CODE:", response.status_code)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print("❌ ERROR decoding JSON:", e)
        print("❌ RESPONSE TEXT:", response.text)
        return []

    recommendations = []
    for item in data.get("tracks", []):
        rec = {
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "image": item["album"]["images"][0]["url"] if item["album"]["images"] else "",
            "preview_url": item["preview_url"],
            "spotify_url": item["external_urls"]["spotify"]
        }
        recommendations.append(rec)

    return recommendations
