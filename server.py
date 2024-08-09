import json
from flask import Flask, request, jsonify
import logging

from dm import do_dm

app = Flask(__name__)

@app.route('/post-json', methods=['POST'])
def receive_json():
    # Get the JSON data from the request
    data = request.get_json()

    # Print the received JSON
    logging.info("Received JSON")
    msg = ""
    if data.get("eventType") == "Download":
        msg += f"# {data.get("series", {}).get("title")}\nDone downloading:\n"
        episodes = data.get("episodes")
        if episodes:
            for ep in episodes:
                msg += f"S{ep.get("seasonNumber")}E{ep.get("episodeNumber")} - {ep.get("title")}"

        do_dm(msg)  # Send the DM
    else:
        msg += "```\n"
        msg += json.dumps(data)
        msg += "\n```"
        do_dm(msg)

    # Respond back to the client
    return jsonify({"status": "success", "received": data}), 200

if __name__ == '__main__':
    app.run(debug=True)
