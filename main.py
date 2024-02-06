import datetime
import os

from flask import Flask, jsonify, request, send_from_directory, json
import random

from poker_logic import evaluate_handV2

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
# Assign a numerical value to each rank for comparison
rank_values = {rank: i for i, rank in enumerate(ranks)}


# User data file
user_data_file = 'user_data.json'

# def load_user_data():
#     try:
#         with open(user_data_file, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}

def load_user_data(user_id):

    try:
        with open(user_data_file, 'r') as file:
            data = json.load(file)
            if user_id in data:
                last_access_time = datetime.datetime.strptime(data[user_id]['last_access'], '%Y-%m-%d %H:%M:%S')
                if (datetime.datetime.now() - last_access_time).days < 1:
                    # User exists and accessed within the last 24 hours
                    return data[user_id]['last_result'], False
            # User doesn't exist or didn't access in the last 24 hours
            return {}, True
    except FileNotFoundError:
        # File not found, so no data exists for any user
        return {}, True

def save_user_data(data):
    with open(user_data_file, 'w') as file:
        json.dump(data, file)


# Generate a random hand
def generate_hand():
    deck = [{'suit': suit, 'rank': rank, 'symbol': suit_symbols[suit] + rank, 'color': 'red' if suit in ['Hearts', 'Diamonds'] else 'black'} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck[:5]

def get_rank_value(card):
    return rank_values[card['rank']]


@app.route('/get-last-result')
def get_last_result():
    user_id = request.remote_addr
    last_result, can_generate_new = load_user_data(user_id)

    if not can_generate_new:
        return jsonify(last_result)
    else:
        return jsonify({'message': 'No previous result found'})



@app.route('/random-hand')
def random_hand():

    user_id = request.remote_addr
    last_result, can_generate_new = load_user_data(user_id)
    user_data = last_result
    if not can_generate_new:
        return jsonify(last_result)

    current_time = datetime.datetime.now()
    #
    # # Check if user has accessed today and return last result if so
    # if user_id in user_data:
    #     last_access_time = datetime.datetime.strptime(user_data[user_id]['last_access'], '%Y-%m-%d %H:%M:%S')
    #     if (current_time - last_access_time).days < 1:
    #         return jsonify(user_data[user_id]['last_result'])

    # Generate and evaluate hand
    hand = generate_hand()
    hand_symbols = [card['symbol'] for card in hand]
    probability, description = evaluate_handV2(hand)

    # Calculate the percentage of hands that are worse than the current hand
    better_than_percentage = 100 - probability
    # 对于高牌，找出最大的牌
    if description.startswith("高牌"):
        highest_card = max(hand, key=get_rank_value)
        highest_card_symbol = highest_card['symbol']
        description = f" ...你今天的运势过于真实，你的最大的牌是 {highest_card_symbol}。"
        message = f'{description} '
    else:
        message = f'你今天的运势是{description}  -超越了 {better_than_percentage:.2f}% 的人。'
    print(hand_symbols, message)

    # Create response
    result = {'hand': hand_symbols, 'probability': probability, 'message': message}

    # Update user data
    user_data[user_id] = {
        'last_access': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'last_result': result
    }
    save_user_data(user_data)

    return jsonify(result)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# 其他路由和函数...

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5050), host='0.0.0.0')