from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import base64
import time
import hashlib
import hmac
import requests
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# Load VAPID keys
with open('vapid_private.pem', 'rb') as f:
    vapid_private_key = serialization.load_pem_private_key(f.read(), password=None)

vapid_public_key_encoded = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZrd0V3WUhLb1pJemowQ0FRWUlLb1pJemowREFRY0RRZ0FFelhkcjh2QWNIb1dkM1YwQ0dGOWhjL21laFVXYwpzZ05lVGJYSlYzTml4YkxqQUVtbFhtaHgzQVhxejZDZlJubStidFVDcVdrK3JycFJrN1hDSm4rdnhRPT0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg"

# Store subscriptions
subscriptions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('', 'service-worker.js')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription = request.json.get('subscription')
    if subscription not in subscriptions:
        subscriptions.append(subscription)
    return jsonify({"message": "Subscription added!"}), 200

@app.route('/send_notification', methods=['POST'])
def send_notification():
    message = request.json.get('message', 'Default message')
    for subscription in subscriptions:
        send_web_push(subscription, message)
    return jsonify({"message": "Notifications sent!"}), 200

def send_web_push(subscription, message):
    endpoint = subscription['endpoint']
    user_agent = "vapid"
    headers = {}
    payload = json.dumps({"title": "New Notification", "body": message}).encode('utf-8')

    # VAPID headers
    expiration = int(time.time()) + 12 * 60 * 60
    claims = {
        "aud": endpoint,
        "exp": expiration,
        "sub": "mailto:your_email@example.com"
    }
    claims_b64 = encode_base64url(json.dumps(claims).encode('utf-8'))
    
    vapid_sig = base64.urlsafe_b64encode(
        hmac.new(
            vapid_private_key.private_numbers().private_value.to_bytes(32, 'big'),
            claims_b64.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).rstrip(b'=').decode('utf-8')
    
    headers['Authorization'] = f'vapid t={claims_b64}, k={vapid_public_key_encoded}'
    headers['Crypto-Key'] = f'p256ecdsa={vapid_public_key_encoded}'
    
    # Send the push notification
    response = requests.post(endpoint, headers=headers, data=payload)
    if response.status_code not in (200, 201):
        print("Failed to send push notification:", response.text)

def encode_base64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
