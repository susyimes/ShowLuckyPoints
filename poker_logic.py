def card_value(card):
    """将牌面转换为数值"""
    value_conversion = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 11,
                        'Queen': 12, 'King': 13, 'Ace': 14}
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
    # sssr
    if is_royal_flush(hand):
        return 0.000154
    # sss
    elif is_straight_flush(hand):
        return 0.00139
    # ssr
    elif is_four_of_a_kind(hand):
        return 0.024
    # ss
    elif is_full_house(hand):
        return 0.14
    # s
    elif is_flush(hand):
        return 0.197
    # a
    elif is_straight(hand):
        return 0.39
    # b
    elif is_three_of_a_kind(hand):
        return 2.11
    # c
    elif is_two_pair(hand):
        return 4.75
    # d
    elif is_one_pair(hand):
        return 42.26
    # e
    else:
        # 如果都不是，则为高牌
        return 50.12

def evaluate_handV2(hand):
        if is_royal_flush(hand):
            return (0.000154, "皇家同花顺0.000154% - 类似于在全球性的大型彩票中赢得数百万美元的头奖，这是一种极其罕见且价值巨大的幸运。【你就是天选之子！】")
        elif is_straight_flush(hand):
            return (0.00139, "同花顺0.00139% - 相当于意外获得了一套开发商提供的房子或者一个免费1年全球游的机会，包括访问多个国家和体验各种文化。【你今天的运势突破天际！】")
        elif is_four_of_a_kind(hand):
            return (0.024, "四条0.024% - 类似于在一次高端汽车品牌的抽奖活动中赢得了一辆全新豪华汽车。【你今天运势无人能比！】")
        elif is_full_house(hand):
            return (0.14, "葫芦0.14% - 可以比作在工作中获得突然的晋升和表彰，或者在一次偶然的会议中结识对未来有巨大影响的人。【你今天福星高照！】")
        elif is_flush(hand):
            return (0.197, "同花0.197% - 像是在一个大型购物平台的活动中意外赢得价值数千美元的购物卡。【你今天运势上上签！】")
        elif is_straight(hand):
            return (0.39, "顺子0.39% - 类似于在一次公司举办的抽奖中赢得了一台最新款的高端电子产品，如最新型号的智能手机或笔记本电脑。【你今天的运势一帆风顺！】")
        elif is_three_of_a_kind(hand):
            return (2.11, "三条2.11% - 像是在一次比赛中获得排名，或者在社交活动中意外结识一位对你有帮助的人。 【你今天的运势上签！】")
        elif is_two_pair(hand):
            return (4.75, "两对4.75% - 这种概率类似于在一个普通的工作日中意外完成一个重要的项目，或者在平凡的一天中收到一个意外的好消息。 【你今天是lucky dog！】")
        elif is_one_pair(hand):
            return (42.26, "一对42.26% - 这种概率比较常见，就像是在一个平凡的日子中享受到一个美好的小惊喜，例如在咖啡店意外获得免费升级的饮料。【 好运喔~】")
        else:
            # 如果都不是，则为高牌
            return (50.12, "高牌 - ...,注意自己手里拿的最大的牌,如果过小可要注意啦")
