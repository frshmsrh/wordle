from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# A dictionary to keep track of game states
game_states = {}
words = ["python", "java", "javascript","socket","izzati"]

def select_word():
    return random.choice(words)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    
    # Initialize game state if not already done
    if room not in game_states:
        word = select_word()
        game_states[room] = {
            'guessed_word': ['_'] * len(word),
            'guessed_letters': [],
            'lives': {},
            'players': [],
            'current_turn': 0,
            'answer': word,
            'game_over': False,
            'message': ''
        }
    
    if username not in game_states[room]['players']:
        game_states[room]['players'].append(username)
        game_states[room]['lives'][username] = 6  # Initial lives for each player
    emit('message', {'msg': f'{username} has joined the room {room}'}, room=room)
    emit('game_state', game_states[room], room=room)

@socketio.on('guess')
def handle_guess(data):
    room = data['room']
    guess = data['guess']
    username = data['username']
    
    if room in game_states and not game_states[room]['game_over']:
        game_state = game_states[room]
        
        # Check if it's the player's turn
        if game_state['players'][game_state['current_turn']] != username:
            emit('message', {'msg': f'It is not your turn.'}, room=room)
            return
        
        # Check if the letter has already been guessed
        if guess in game_state['guessed_letters']:
            emit('message', {'msg': f'{username}, you already guessed the letter "{guess}".'}, room=room)
        else:
            game_state['guessed_letters'].append(guess)
            
            # Check if the guess is in the answer
            if guess in game_state['answer']:
                for idx, letter in enumerate(game_state['answer']):
                    if letter == guess:
                        game_state['guessed_word'][idx] = guess
                
                # Check if the word is completely guessed
                if '_' not in game_state['guessed_word']:
                    game_state['game_over'] = True
                    game_state['message'] = f'Congratulations {username}! You guessed the word: {game_state["answer"]}'
                    emit('message', {'msg': game_state['message']}, room=room)
            else:
                game_state['lives'][username] -= 1
                # Check if the player's game is over
                if game_state['lives'][username] <= 0:
                    game_state['game_over'] = True
                    game_state['message'] = f'{username}, you lost! The correct word was: {game_state["answer"]}'
                    emit('message', {'msg': game_state['message']}, room=room)
            
            # Move to the next turn
            game_state['current_turn'] = (game_state['current_turn'] + 1) % len(game_state['players'])
            emit('game_state', game_states[room], room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    game_state = game_states[room]
    if username in game_state['players']:
        game_state['players'].remove(username)
        if game_state['players']:
            game_state['current_turn'] = game_state['current_turn'] % len(game_state['players'])
        else:
            game_state['game_over'] = True
            game_state['message'] = 'Game over! All players left the room.'
    emit('message', {'msg': f'{username} has left the room {room}'}, room=room)
    emit('game_state', game_states[room], room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
