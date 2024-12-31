URL Shortener API
This Flask application provides a simple REST API for shortening URLs. It uses an in-memory store for demonstration purposes; for production, a persistent database is required.

Endpoints
POST /shorten: Accepts a JSON payload { "url": "long_url" } and returns { "short_url": "shortened_url" }.
GET /<short_code>: Redirects to the original URL associated with the given short code. Returns 404 if the code is invalid.
