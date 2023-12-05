from flask import Flask, request, jsonify, render_template
import random
import threading

app = Flask(__name__)

# Thread lock for concurrency control
lock = threading.Lock()

# Participants list
initial_participants = ['Olek', 'Sandra', 'Igor', 'Monika', 'Ania', 'Filip']
participants = initial_participants.copy()
drawn_by = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/draw', methods=['POST'])
def draw():
    with lock:
        name = request.json.get('name')
        if name in drawn_by:
            return jsonify({'error': f'{name} Już wylosowałeś/aś kogoś!'}), 400
        available = [p for p in participants if p != name]
        if not available:
            return jsonify({'message': 'Nie ma już kogo wylosować :()'}), 200
        selected = random.choice(available)
        participants.remove(selected)
        drawn_by.append(name)
        return jsonify({'drawnName': selected})

@app.route('/reset', methods=['POST'])
def reset():
    global participants, drawn_by
    participants = initial_participants.copy()
    drawn_by = []
    return jsonify({'message': 'Resetowanie! Tylko dla admina!'})

if __name__ == '__main__':
    app.run(debug=True)
