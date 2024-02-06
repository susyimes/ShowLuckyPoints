def card_value(card):
    """将牌面转换为数值"""
    value_conversion = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
    return value_conversion[card['rank']]



def is_flush(hand):
    """检查是否为同花"""
    suits = [card['suit'] for card in hand]
    return len(set(suits)) == 1


def is_straight(hand):
    """检查是否为顺子"""
    values = sorted([card_value(card) for card in hand])
    for i in range(4):
        if values[i + 1] - values[i] != 1:
            return False
    return True


def is_royal_flush(hand):
    """检查是否为皇家同花顺"""
    if not is_flush(hand):
        return False
    values = sorted([card_value(card) for card in hand])
    return values == [10, 11, 12, 13, 14]


def is_straight_flush(hand):
    """检查是否为同花顺"""
    return is_flush(hand) and is_straight(hand)


def is_four_of_a_kind(hand):
    """检查是否为四条"""
    values = [card_value(card) for card in hand]
    return any(values.count(value) == 4 for value in values)


def is_full_house(hand):
    values = [card['rank'] for card in hand]
    value_counts = {value: values.count(value) for value in set(values)}
    return sorted(value_counts.values()) == [2, 3]


def is_three_of_a_kind(hand):
    values = [card['rank'] for card in hand]
    return any(values.count(value) == 3 for value in values)


def is_two_pair(hand):
    values = [card['rank'] for card in hand]
    pairs = [value for value in set(values) if values.count(value) == 2]
    return len(pairs) == 2


def is_one_pair(hand):
    values = [card['rank'] for card in hand]
    return any(values.count(value) == 2 for value in values)


def evaluate_hand(hand):
    if is_royal_flush(hand):
        return 0.000154
    elif is_straight_flush(hand):
        return 0.00139
    elif is_four_of_a_kind(hand):
        return 0.024
    elif is_full_house(hand):
        return 0.14
    elif is_flush(hand):
        return 0.197
    elif is_straight(hand):
        return 0.39
    elif is_three_of_a_kind(hand):
        return 2.11
    elif is_two_pair(hand):
        return 4.75
    elif is_one_pair(hand):
        return 42.26
    else:
        # 如果都不是，则为高牌
        return 50.12
