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
    
@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    url_data = urls_collection.find_one({'shortCode': short_code})
    
    if not url_data:
        return jsonify({'error': 'Short URL not found'}), 404
    
    # Increment access count
    urls_collection.update_one(
        {'_id': url_data['_id']},
        {'$inc': {'accessCount': 1}}
    )
    
    return jsonify({
        'id': str(url_data['_id']),
        'url': url_data['url'],
        'shortCode': url_data['shortCode'],
        'createdAt': url_data['createdAt'],
        'updatedAt': url_data['updatedAt'],
        'accessCount': url_data['accessCount'] + 1
    }), 200
    
@app.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    data = request.get_json()
    new_url = data.get('url')

    if not new_url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not validate_url(new_url):
        return jsonify({'error': 'Invalid URL'}), 400

    url_data = urls_collection.find_one({'shortCode': short_code})
    if not url_data:
        return jsonify({'error': 'Short URL not found'}), 404

    now = datetime.utcnow()
    urls_collection.update_one(
        {'shortCode': short_code},
        {'$set': {
            'url': new_url,
            'updatedAt': now
        }}
    )

    updated_url = urls_collection.find_one({'shortCode': short_code})
    
    return jsonify({
        'id': str(updated_url['_id']),
        'url': updated_url['url'],
        'shortCode': updated_url['shortCode'],
        'createdAt': updated_url['createdAt'],
        'updatedAt': updated_url['updatedAt']
    }), 200