from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("REBRICKABLE_API_KEY")
if not API_KEY:
    raise RuntimeError("REBRICKABLE_API_KEY not set")

BASE_URL = "https://rebrickable.com/api/v3/lego/sets/"

app = Flask(__name__)

def fetch_set(set_num):
    headers = {"Authorization": f"key {API_KEY}"}
    url = f"{BASE_URL}{set_num}/"
    r = requests.get(url, headers=headers, timeout=5)

    if r.status_code == 404:
        return None

    r.raise_for_status()
    return r.json()

@app.route("/sets/<set_num>")
def get_set(set_num):
    s = fetch_set(set_num)
    if not s:
        return jsonify({"error": "Invalid set number"}), 404

    return jsonify({
        "set_name": s["name"],
        "set_num": s["set_num"],
        "year": s["year"],
        "pieces": s["num_parts"],
        "image": s["set_img_url"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
