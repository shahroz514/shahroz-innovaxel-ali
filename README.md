
# URL Shortener

A Flask-based URL shortening service with MongoDB.

## Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or remote)
- pip

### Installation
1. Clone the repository:
   
   git clone https://github.com/shahroz514/shahroz-innovaxel-ali.git
   cd url-shortener
Install dependencies:


pip install -r requirements.txt
Set up environment:


echo "MONGO_URI=mongodb://localhost:27017/" > .env
Running the Application
Start MongoDB service (if local)

Run the Flask app:

python app.py
Access the web interface at:

http://localhost:5000
Using the API
Base URL: http://localhost:5000

Endpoints:

POST /shorten - Create short URL

GET /<short_code> - Redirect to original URL

PUT /shorten/<short_code> - Update destination URL

DELETE /shorten/<short_code> - Delete short URL

GET /shorten/<short_code>/stats - Get access stats

