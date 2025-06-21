import os
from flask import Flask, render_template, request, jsonify
from spotify_client import search_track

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]

    # Call the Spotify search
    results = search_track(user_input)

    if "error" in results:
        reply = "🤖 Sorry, I couldn't connect to Spotify right now."
    elif results.get("tracks") and results["tracks"]["items"]:
        reply = "🎵 Here are some tracks you might like:\n"
        for item in results["tracks"]["items"]:
            name = item["name"]
            artist = item["artists"][0]["name"]
            album_art = item["album"]["images"][0]["url"]
            link = item["external_urls"]["spotify"]
            reply += f"<br><strong>{name}</strong> by {artist} <br><a href='{link}' target='_blank'><img src='{album_art}' width='100'></a><br><br>"
    else:
        reply = "🤖 Sorry, I couldn't find any songs related to that."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
