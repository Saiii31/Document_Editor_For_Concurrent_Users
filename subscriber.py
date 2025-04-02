import redis
import json

def listen_updates():
    try:
        redis_client = redis.Redis(
            host='redis-18748.c52.us-east-1-4.ec2.redns.redis-cloud.com',
            port=18748,
            username="default",
            password="cvvwk0fJdtANV5YImp41DljgYhIKplav",
            decode_responses=True
        )
        pubsub = redis_client.pubsub()
        pubsub.subscribe('document_updates')

        print("Listening for document updates...")
        for message in pubsub.listen():
            if message['type'] == 'message':
                try:
                    update_data = json.loads(message['data'])  # Parse JSON
                    print(f"Update received: {update_data['user']} - {update_data['text']}")
                except Exception as e:
                    print(f"Error parsing message: {e}")

    except redis.RedisError as e:
        print(f"Redis connection error: {e}")

if __name__ == "__main__":
    listen_updates()
