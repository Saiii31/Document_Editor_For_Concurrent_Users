"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-18748.c52.us-east-1-4.ec2.redns.redis-cloud.com',
    port=18748,
    decode_responses=True,
    username="default",
    password="cvvwk0fJdtANV5YImp41DljgYhIKplav",
    
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

# redis-cli -h redis-18748.c52.us-east-1-4.ec2.redns.redis-cloud.com -p 18748 -a cvvwk0fJdtANV5YImp41DljgYhIKplav