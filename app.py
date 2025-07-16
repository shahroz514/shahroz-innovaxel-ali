from flask import Flask, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import shortuuid
import validators
from config import Config
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['DB_NAME']]
urls_collection = db['urls']

def generate_short_code():
    return shortuuid.ShortUUID().random(length=6)

def validate_url(url):
    return validators.url(url)

@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not validate_url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    # Check if URL already exists
    existing_url = urls_collection.find_one({'url': original_url})
    if existing_url:
        return jsonify({
            'id': str(existing_url['_id']),
            'url': existing_url['url'],
            'shortCode': existing_url['shortCode'],
            'createdAt': existing_url['createdAt'],
            'updatedAt': existing_url['updatedAt'],
            'shortUrl': f"{app.config['BASE_URL']}{existing_url['shortCode']}"
        }), 200

    short_code = generate_short_code()
    now = datetime.utcnow()

    url_data = {
        'url': original_url,
        'shortCode': short_code,
        'createdAt': now,
        'updatedAt': now,
        'accessCount': 0
    }

    result = urls_collection.insert_one(url_data)
    
    return jsonify({
        'id': str(result.inserted_id),
        'url': original_url,
        'shortCode': short_code,
        'createdAt': now,
        'updatedAt': now,
        'shortUrl': f"{app.config['BASE_URL']}{short_code}"
    }), 201