import os

from flask import Flask, jsonify, send_from_directory
import random

from poker_logic import evaluate_hand, card_value

app = Flask(__name__)
suit_symbols = {
    'Hearts': '♥',
    'Diamonds': '♦',
    'Clubs': '♣',
    'Spades': '♠'
}
# Poker card definitions
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Generate a random hand
def generate_hand():
    deck = [{'suit': suit, 'rank': rank, 'symbol': suit_symbols[suit] + rank, 'color': 'red' if suit in ['Hearts', 'Diamonds'] else 'black'} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck[:5]

# Route for random hand
@app.route('/random-hand')
def random_hand():
    try:
        hand = generate_hand()
        hand_symbols = [card['symbol'] for card in hand]
        probability = evaluate_hand(hand)

        # Calculate the percentage of hands that are worse than the current hand
        better_than_percentage = 100 - probability

        # Create a message that includes this information
        message = f'这手牌的概率是 {probability:.2f}%, 超越了 {better_than_percentage:.2f}% 的人。'

        print(hand_symbols, message)
        return jsonify({'hand': hand_symbols, 'probability': probability, 'message': message})
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)})


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# 其他路由和函数...

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5050), host='0.0.0.0')