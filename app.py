import os
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

anger_start = None
UNHEALTHY_TIMEOUT = 15   # after this, /health reports unhealthy
CRASH_TIMEOUT = 25       # after this, process exits
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
    anger_start = time.time() if mood == "angry" else None
    return jsonify({"mood": mood})

@app.route('/health')
def health():
    elapsed = get_anger_time()

    if mood == "angry" and elapsed > CRASH_TIMEOUT:
        response = jsonify({"status": "unhealthy", "mood": mood, "anger_time": elapsed})
        response.status_code = 503

        @response.call_on_close
        def crash():
            os._exit(1)

        return response

    if mood == "angry" and elapsed > UNHEALTHY_TIMEOUT:
        return jsonify({"status": "unhealthy", "mood": mood, "anger_time": elapsed}), 503

    return jsonify({"status": "healthy", "mood": mood, "anger_time": elapsed})

def get_anger_time():
    if mood == "angry" and anger_start:
        return round(time.time() - anger_start, 1)
    return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    