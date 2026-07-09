import os
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Track when anger started
anger_start = None
ANGER_TIMEOUT = 30  # seconds until crash

# Current mood
mood = "calm"

@app.route('/')
def index():
    return render_template('index.html', mood=mood)

@app.route('/mood')
def get_mood():
    return jsonify({"mood": mood, "anger_time": get_anger_time()})

@app.route('/set/<new_mood>')
def set_mood(new_mood):
    global mood, anger_start
    mood = new_mood
    if mood == "angry":
        anger_start = time.time()
    else:
        anger_start = None
    return jsonify({"mood": mood})

@app.route('/health')
def health():
    if mood == "angry" and anger_start:
        elapsed = time.time() - anger_start
        if elapsed > ANGER_TIMEOUT:
            # Simulate crash
            return jsonify({"status": "unhealthy", "reason": "too angry"}), 500
    return jsonify({"status": "healthy", "mood": mood})

def get_anger_time():
    if mood == "angry" and anger_start:
        return round(time.time() - anger_start, 1)
    return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)