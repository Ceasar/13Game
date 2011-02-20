import random

def new_deck():
    """Create a new deck."""
    cards = []
    mydict = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace", 15: "2"}
    for x in range(3,16):
        name = str(x)
        pip = 4*(x-3)
        if x in mydict:
            name = mydict[x]
        cards.append(Card(name, "Spades", pip))
        cards.append(Card(name, "Clovers", pip+1))
        cards.append(Card(name, "Diamonds", pip+2))
        cards.append(Card(name, "Hearts", pip+3))
    return cards

class Card():
    """Represent a simple playing card."""
    def __init__(self, name, suit, pip):
        self.name = name
        self.suit = suit
        self.pip = pip

    def __str__(self):
        return self.name + " of " + self.suit


class Deck():
    """Simulate a deck of cards."""
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self, hand, n=13):
        """Deal n cards from the Deck to a particular hand."""
        for x in range(n):
            hand.cards.append(self.cards[0])
            self.cards.remove(self.cards[0])

    def reveal(self, n=13):
        """Deal n cards from the Deck to a particular hand."""
        return [self.cards[x] for x in range(n)]

    def __str__(self):
        return "".join([str(card)+"\n" for card in self.cards])

class Hand():
    def __init__(self):
        self.cards = []

    def sort(self):
        """Sort the hand from highest to lowest."""
        self.cards = sorted(self.cards, key = lambda card: card.pip)

    def __str__(self):
        toprint = ""
        for index, card in enumerate(self.cards):
            toprint += str(index + 1) + ": " + str(card)+"\n"
        return toprint

def sample_hand(deck, n=13):
    """Generate a sample hand from a deck."""
    hand = Hand()
    random.shuffle(deck)
    hand.cards = deck[0:n]
    hand.sort()
    return hand

def is_straight(cards):
    """Check to see if the cards are straight."""
    length = len(cards)
    if length > 1 and cards[length - 1].name != str(2):
        if cards[length - 1].pip / 4 - 1 == cards[length - 2].pip / 4:
            if length > 2:
                return is_straight(cards[0:length-1])
            return True
    return False

def get_straights(hand):
    """Find all the straights in a Hand."""
    mydict = {}
    for x in range(3,13):
        mydict[x] = []
    current = hand.cards[0]
    straight = [current]
    for card in hand.cards:
        if card.pip/4 == 12:
            break
        difference = card.pip / 4 - current.pip / 4
        current = card
        if difference == 1:
            straight.append(card)
        if difference > 1:
            if len(straight) > 2:
                mydict[len(straight)].append(straight)
            straight = [current]
    if len(straight) > 2:
        mydict[len(straight)].append(straight)
    return mydict

def test_get_straights():
    """Test the get_straights function."""
    b = sample_hand(new_deck())
    c = get_straights(b)
    print b
    for x in b.cards:
        print x.pip/4
    for x in c.values():
        for y in x:
            print y
        print ""

def is_tuple(cards, n=-1):
    """Check to see if the cards are the same."""
    if (n == -1):
        n = len(cards)
    if (n > 1):
        if (cards[n - 1].name == cards[n - 2].name):
            if (n>2):
                return is_tuple(cards,n-1)
            return True
    return False

def get_tuples(hand):
    """Find all the straights in a Hand."""
    mydict = {}
    for x in range(2,5):
        mydict[x] = []
    current = hand.cards[0]
    tuple_ = [] 
    for card in hand.cards:
        if card.name != current.name:
            if len(tuple_) > 1:
                mydict[len(tuple_)].append(tuple_)
            tuple_ = []
        tuple_.append(card)
        current = card
    if len(tuple_) > 1:
        mydict[len(tuple_)].append(tuple_)
    return mydict

def test_get_tuples():
    """Test the get_tuples function."""
    b = sample_hand(new_deck())
    c = get_tuples(b)
    print b
    for x in c.values():
        for y in x:
            for z in y:
                print z
            print ""

def test():
    a = sample_hand(new_deck())
    print a
    b = get_tuples(a)
    c = get_straights(a)
    for x in b.values():
        for y in x:
            for z in y:
                print z
            print ""
    for x in c.values():
        for y in x:
            for z in y:
                print z
            print ""
