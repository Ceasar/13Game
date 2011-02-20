from playingcards import *

def sample_straights(deck, e=13, n=1000):
    """Generate a dictionary populated with sample straights."""
    data = {}
    for x in range(3, 13):
        data[x] = []
    for x in range(n):
        hand = sample_hand(deck, e)
        straights = get_straights(hand)
        for key in straights.keys():
            data[key] += straights[key]
    return data

def sample_tuples(deck, e=13, n=1000):
    """Generate a dictionary populated with sample tuples."""
    data = {}
    for x in range(2, 5):
        data[x] = []
    for x in range(n):
        hand = sample_hand(deck, e)
        tuples = get_tuples(hand)
        for key in tuples.keys():
            data[key] += tuples[key]
    return data

def chance_to_play(cards, deck, e=13, n=1000):
    """Get the probability that the opponent can match the cards."""
    if is_straight(cards):
        print "straight"
        return len(sample_straights(deck, n)[len(cards)]) / float(n)
    elif is_tuple(cards):
        return len(sample_tuples(deck, n)[len(cards)]) / float(n)
    elif len(cards) == 1:
        return 1.0

def chance_to_win(cards, deck, e=13, n=1000):
    """Get the chance to win for a particular set of cards."""
    highpip = cards[len(cards) - 1].pip
    if len(cards) == 1:
        for x in range(n):
            hand = sample_hand(new_deck())
            for card in hand.cards:
                if card.pip > highpip:
                    better.append([card])
                    break
        return 1 - (len(better) / float(n))
    elif is_straight(cards):
        func = sample_straights
    elif is_tuple(cards):
        func = sample_tuples
    better = []
    for data in func(deck, n)[len(cards)]:
        if data[len(data) - 1].pip > highpip:
            better.append(data)
            break
    return 1 - (len(better) / float(n))


def analyze(cards, deck, e=13, n=2500):
    """Generate a tuple containing the cards entered, the probability
    the opponent can match it, and the probability it will win."""
    highpip = cards[len(cards) - 1].pip
    better = []
    if len(cards) == 1:
        for x in range(n):
            hand = sample_hand(deck, e)
            for card in hand.cards:
                if card.pip > highpip:
                    better.append([card])
        return (cards, 1.0, 1 - (len(better) / float(n*e)))
    elif is_straight(cards):
        func = sample_straights
    elif is_tuple(cards):
        func = sample_tuples
    dataset = func(deck, e, n)[len(cards)]
    for data in dataset:
        if data[len(data) - 1].pip > highpip:
            better.append(data)
    return (cards, len(dataset) / float(n), 1.00 - (len(better) / float(len(dataset))))
