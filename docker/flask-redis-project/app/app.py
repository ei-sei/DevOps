# Flask is the web framework - handles routing and HTTP requests
from flask import Flask
# redis-py is the Python client library for talking to Redis
import redis

# Create the Flask app instance
app = Flask(__name__)

# Connect to Redis - 'redis' resolves to the Redis container via Docker Compose networking
# decode_responses=True returns strings instead of raw bytes
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Route for the home page - returns a welcome message with a link to the counter
@app.route('/')
def home():
    return '''
        <h4>Welcome to Flask + Redis!</h4>
        <a href="/count"><button>Go to Counter</button></a>
    '''

# Route for the counter - every visit increments the count in Redis
@app.route('/count')
def count():
    # INCR atomically increments 'visit_count' by 1 and returns the new value
    # If the key doesn't exist yet, Redis creates it starting at 0 before incrementing
    visit_count = redis_client.incr('visit_count')
    return f'Visit count: {visit_count}'

# Only runs when executed directly (not when imported or run via a WSGI server)
# 0.0.0.0 makes the app reachable from outside the container
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

