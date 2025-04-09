from flask import Flask, render_template, request, jsonify
import redis
import threading
import json
import os
import subprocess

# Start subscriber.py in background
subprocess.Popen(["python", "subscriber.py"])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Redis configuration
redis_client = redis.Redis(
    host='redis-18748.c52.us-east-1-4.ec2.redns.redis-cloud.com',
    port=18748,
    username="default",
    password="cvvwk0fJdtANV5YImp41DljgYhIKplav",
    decode_responses=True
)

# Redis Subscriber Function
def redis_subscriber():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('document_updates')

    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                update_data = json.loads(message['data'])
                print("Received update (but SocketIO disabled):", update_data)
                # If needed: Store this in a DB, or log to file
            except Exception as e:
                print("Error reading update:", e)

# Run Redis listener in background
threading.Thread(target=redis_subscriber, daemon=True).start()

@app.route('/')
def index():
    document_data = redis_client.hgetall("document:123")
    return render_template('index.html', document_data=document_data)

@app.route('/edit', methods=['POST'])
def edit_document():
    user_id = request.form['user_id']
    changes = request.form['changes']

    redis_client.hset("document:123", user_id, changes)
    update_data = {"user": user_id, "text": changes}
    redis_client.publish('document_updates', json.dumps(update_data))

    return jsonify(update_data)

@app.route('/update', methods=['POST'])
def update_document():
    data = request.json
    user_id = data.get("user_id")
    changes = data.get("changes")

    if not user_id or not changes:
        return jsonify({"error": "Invalid data"}), 400

    redis_client.hset("document:123", user_id, changes)
    update_data = {"user": user_id, "text": changes}
    redis_client.publish('document_updates', json.dumps(update_data))

    return jsonify({"message": "Document updated"})

@app.route('/view-data')
def view_data():
    document_data = redis_client.hgetall("document:123")
    return jsonify(document_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
