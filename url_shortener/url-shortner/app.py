from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)


# Create the table
with app.app_context():
    db.create_all()

    def __repr__(self):
        return f'<URL {self.original_url} -> {self.short_code}>'

def generate_short_code():
    """Generates a unique short code."""
    while True:
        short_code = "".join(secrets.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(6))
        existing_url = URL.query.filter_by(short_code=short_code).first()
        if not existing_url:
            return short_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']
    short_code = generate_short_code()
    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    short_url = f"{request.host_url}{short_code}" 
    return render_template('shorten_result.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_original(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.original_url)
    else:
        return render_template('404.html'), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        # Populate the database with initial data
        sample_urls = [
            ("https://www.example.com", generate_short_code()),
            ("https://www.anotherexample.com", generate_short_code()),
            ("https://www.yetanotherexample.com", generate_short_code())
        ]
        
        for original_url, short_code in sample_urls:
            new_url = URL(original_url=original_url, short_code=short_code)
            db.session.add(new_url)
        
        db.session.commit()

    app.run(debug=True)
