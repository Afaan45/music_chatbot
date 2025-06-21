import os
from flask import Flask, render_template, request, jsonify
from spotify_client import get_token, search_track, get_recommendations

app = Flask(__name__)

collections = {}

@app.route('/')
def index():
    return render_template('index.html', collections=list(collections.keys()), current_collection=None, tracks=[])

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get("query", "")
    token = get_token()

    if not query:
        return jsonify([])

    results = search_track(query, token)
    return jsonify(results)

@app.route('/create_collection', methods=['POST'])
def create_collection():
    data = request.json
    name = data.get("name", "").strip()

    if name and name not in collections:
        collections[name] = []

    return jsonify({"collections": list(collections.keys())})

@app.route('/add_to_collection', methods=['POST'])
def add_to_collection():
    data = request.json
    collection = data.get("collection")
    track = data.get("track")

    if collection and track:
        collections[collection].append(track)

    return jsonify({"status": "success"})

@app.route('/view_collection', methods=['POST'])
def view_collection():
    data = request.json
    collection = data.get("collection")

    tracks = collections.get(collection, [])
    return jsonify({"tracks": tracks})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    collection = data.get("collection")
    tracks = collections.get(collection, [])

    if not tracks:
        return jsonify([])

    last_track = tracks[-1]
    last_track_id = last_track.get("id")
    artist_id = last_track.get("artist_id")
    genre = last_track.get("genre") or "pop"

    print("📡 RECOMMEND INPUT:")
    print("Track ID:", last_track_id)
    print("Artist ID:", artist_id)
    print("Genre:", genre)

    token = get_token()
    recs = get_recommendations(track_id=last_track_id, artist_id=artist_id, genre=genre, token=token)

    return jsonify(recs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
