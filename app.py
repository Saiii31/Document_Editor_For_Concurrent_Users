from flask import Flask, render_template, request,jsonify
from flask_socketio import SocketIO, emit
import redis
import threading
import json
import config  # Import config.py

app = Flask(__name__)

# Configure Redis connection


app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000")

# Initialize Redis client
redis_client = redis.Redis(
    host='redis-18748.c52.us-east-1-4.ec2.redns.redis-cloud.com',
    port=18748,
    decode_responses=True,
    username="default",
    password="cvvwk0fJdtANV5YImp41DljgYhIKplav",
)

# Redis Pub/Sub Subscriber to listen for changes and emit updates
def redis_subscriber():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('document_updates')  # Subscribe to the document updates channel

    for message in pubsub.listen():
        if message['type'] == 'message':
            # Emit the update to all WebSocket clients
            socketio.emit('document_update', message['data'])

# Start the subscriber in a separate thread
threading.Thread(target=redis_subscriber, daemon=True).start()

@app.route('/')
def index():
    # Fetch the document data from Redis
    document_data = redis_client.hgetall("document:123")
    return render_template('index.html', document_data=document_data)

@app.route('/edit', methods=['POST'])
@app.route('/edit', methods=['POST'])
def edit_document():
    user_id = request.form['user_id']
    changes = request.form['changes']

    # Save the changes to Redis hash (HSET to store user changes)
    redis_client.hset("document:123", user_id, changes)

    # Publish an update to the Redis channel
    redis_client.publish('document_updates', f"User {user_id} made changes")

    # Send a JSON response back to the front-end
    return {'user': user_id, 'message': changes}



@app.route('/update', methods=['POST'])
def update_document():
    data = request.json
    user_id = data.get("user_id")
    changes = data.get("changes")

    if not user_id or not changes:
        return jsonify({"error": "Invalid data"}), 400

    redis_client.hset("document:123", user_id, changes)
    stored_data = redis_client.hgetall("document:123")
    print("Stored Data in Redis:", stored_data)  

    return jsonify({"message": "Document updated"})

@app.route('/view-data')
def view_data():
    
    document_data = redis_client.hgetall("document:123")
    return jsonify(document_data)


@socketio.on('connect')
def on_connect():
    print("User connected")

@socketio.on('disconnect')
def on_disconnect():
    print("User disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True)
