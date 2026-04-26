from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return '''
    <h1>Lab 01 - Docker Pipeline</h1><p>Flask app running in a container.</p>
    <a href="/health"><button>Health</button></a>
    '''


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
