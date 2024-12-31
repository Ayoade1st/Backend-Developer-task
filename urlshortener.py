from flask import Flask, request, jsonify, redirect, url_for
from collections import defaultdict
import secrets
app = Flask(__name__)
# In-memory dictionary to store short codes and long URLs
url_map = defaultdict(str) # Use defaultdict to avoid KeyError for missing keys

# SHORT URL for shortened URLs
short_url = "http://localhost:5000/"

# Secret key for URL shortening 
secret_key = secrets.token_urlsafe(32)

import hashlib
def shorten_url(url):
    """
    Generates a unique short code for the given long URL.
    """
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:6] # Truncate hash for shorter code
    short_code = short_url + url_hash
    # Check for conflicts and regenerate if needed (unlikely with short hash)
    while short_code in url_map:
        url_hash = hashlib.sha256(url_hash.encode()).hexdigest()[:6]
        short_code = base_url + url_hash
    return short_code

@app.route('/shorten', methods=['POST'])
def create_short_url():
    url_data = request.get_json()
    if not url_data or not url_data.get("url"):
        return jsonify({'error': 'Missing required field "url"'}), 400

    long_url = url_data["url"]
    short_code = shorten_url(long_url)
    url_map[short_code] = long_url
    return jsonify({'short_url': short_code})

@app.route('/<short_code>')
def redirect_to_original(short_code):
    long_url = url_map.get(short_code)
    if not long_url:
        return jsonify({'error': 'Short code not found'}), 404
    return redirect(long_url)


if __name__ == '__main__':
    app.run(debug=True)
