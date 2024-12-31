from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
import secrets

app = Flask(__name__, static_folder='frontend', static_url_path='/')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

secret_key = secrets.token_urlsafe(32)

class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    original_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<URLMap {self.short_code} -> {self.original_url}>'

def shorten_url(url):
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:6]
    return url_hash

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

@app.route('/shorten', methods=['POST'])
def create_short_url():
    url_data = request.get_json()
    if not url_data or not url_data.get("url"):
        return jsonify({'error': 'Missing required field "url"'}), 400

    long_url = url_data["url"]
    short_code = shorten_url(long_url)

    existing_url = URLMap.query.filter_by(short_code=short_code).first()
    if existing_url:
        return jsonify({'short_url': url_for('.redirect_to_original', short_code=short_code)}), 200

    new_url_map = URLMap(short_code=short_code, original_url=long_url)
    db.session.add(new_url_map)
    db.session.commit()

    return jsonify({'short_url': url_for('.redirect_to_original', short_code=short_code)})

@app.route('/<short_code>')
def redirect_to_original(short_code):
    url_map = URLMap.query.filter_by(short_code=short_code).first()
    if not url_map:
        return jsonify({'error': 'Short code not found'}), 404
    return redirect(url_map.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)