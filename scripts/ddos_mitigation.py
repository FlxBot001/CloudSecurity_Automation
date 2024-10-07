from flask import Flask, request, jsonify
import redis
import time
import os
import logging
from functools import wraps
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration settings (can be set through environment variables)
RATE_LIMIT = int(os.getenv('RATE_LIMIT', 10))  # max requests
TIME_WINDOW = int(os.getenv('TIME_WINDOW', 60))  # time window in seconds
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Connect to Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Load pre-trained DDoS classification model
model = joblib.load("ml/models/ddos_model.pkl")

def rate_limit(limit, period):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ip_address = request.remote_addr

            # Check if the IP is whitelisted
            if is_whitelisted(ip_address):
                return func(*args, **kwargs)

            # Use Redis to track requests
            current_time = time.time()
            redis_key = f"rate_limit:{ip_address}"

            # Increment the request count
            current_count = redis_client.get(redis_key)

            # If the count doesn't exist, set it
            if current_count is None:
                redis_client.set(redis_key, 1, ex=period)  # Set key with expiration
                logger.info(f"IP {ip_address} has made its first request.")
            else:
                current_count = int(current_count)
                if current_count >= limit:
                    logger.warning(f"IP {ip_address} exceeded rate limit.")
                    return jsonify({"error": "Too many requests. Please try again later."}), 429
                else:
                    redis_client.incr(redis_key)
                    logger.info(f"IP {ip_address} has made a request. Count: {current_count + 1}")

            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_whitelisted(ip_address):
    # Define a list of whitelisted IPs
    whitelisted_ips = ["192.168.1.1", "127.0.0.1"]  # Modify this list as needed
    return ip_address in whitelisted_ips

@app.route('/api', methods=['GET'])
@rate_limit(RATE_LIMIT, TIME_WINDOW)
def api():
    return jsonify({"message": "Welcome to the DDoS Classification API!"})

@app.route('/classify', methods=['POST'])
@rate_limit(RATE_LIMIT, TIME_WINDOW)
def classify_ddos():
    # Expecting JSON input with traffic data features
    data = request.json
    required_features = ['packet_size', 'protocol', 'src_port', 'dst_port', 'timestamp']

    if not all(feature in data for feature in required_features):
        return jsonify({"error": "Missing required features."}), 400

    # Convert incoming data to DataFrame for prediction
    input_data = pd.DataFrame([data])
    
    # Perform classification using the loaded model
    prediction = model.predict(input_data)
    
    # Map prediction to meaningful labels
    classification_result = "DDoS Attack" if prediction[0] == 1 else "Normal Traffic"
    
    return jsonify({"classification": classification_result})

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({
        "rate_limit": RATE_LIMIT,
        "time_window": TIME_WINDOW
    })

@app.route('/config', methods=['POST'])
def set_config():
    global RATE_LIMIT, TIME_WINDOW
    data = request.json
    if 'rate_limit' in data:
        RATE_LIMIT = data['rate_limit']
    if 'time_window' in data:
        TIME_WINDOW = data['time_window']
    return jsonify({"message": "Configuration updated.", "rate_limit": RATE_LIMIT, "time_window": TIME_WINDOW})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
