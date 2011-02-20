import math
import copy
from analyzer import *
from playingcards import *

#Remove caps from non-class names. No camel case, underscores instead.
#Use plurals in list. No 'x' variable names. Docstrings.
#Initialize all variables in init.

def display():
    print table
    print "Your hand:"
    print table.players[0].hand
    print "Play cards by typing play([x,y,...,z])"
    

def get_options(hand):
    """Get a list of all the possible tuples that can be played."""
    options = []
    legal_options = []
    count = len(table.cards)
    if count == 0:
        [options.append([x]) for x in hand.cards]
        for rank in get_tuples(hand).values():
            for tuple_ in rank:
                options.append(tuple_)
        for rank in get_straights(hand).values():
            for straight in rank:
                options.append(straight)
        return options
    elif len(table.cards) == 1:
        [options.append([x]) for x in hand.cards]
    elif is_tuple(table.cards):
        for tuple_ in get_tuples(hand)[len(table.cards)]:
            options.append(tuple_)
    elif is_straight(table.cards):
        for straight in get_straights(hand)[len(table.cards)]:
            options.append(straight)
    for option in options:
        if option[len(option) - 1].pip > table.cards[count - 1].pip:
            legal_options.append(option)
    return legal_options


class Player(object):
    def __init__(self, money, name):
        self.name = name
        self.money = money
        self.hand = Hand()
        self.turn = False

    def play(self, numbers):
        """Play a set of a cards."""
        cards = []
        for number in numbers:
            cards.append(self.hand.cards[number - 1])
        if (table.validate(cards)):
            self.turn = False
            table.cards = cards
            for card in cards:
                self.hand.cards.remove(card)
            print self.name + " played:"
            print table
            ai.think()
        else:
            print "That's illegal."
        
    def skip(self):
        """Exit the round."""
        print self.name + " passed."
        table.cards = []
        print table
        ai.think()

    def __str__(self):
        return self.name


class AI():
    def __init__(self, money, name):
        self.name = name
        self.money = money
        self.hand = Hand()
        self.turn = False
        self.e = 13
        self.unknowns = new_deck()

    def calibrate(self):
        """Calibrates the AI's idea of the deck."""
        for card in self.hand.cards:
            for unknown in self.unknowns:
                if str(card) == str(unknown):
                    self.unknowns.remove(unknown)
                    break

    def play(self, cards):
        """Play a set of cards."""
        self.turn = False
        for card in cards:
            if card not in self.hand.cards:
                return
        if (table.validate(cards)):
            table.cards = cards
            print self.name + " played:"
            for card in cards:
                self.hand.cards.remove(card)
            display()

    def skip(self):
        """Exit the round."""
        print self.name + " passed."
        table.cards = []
        display()

    def think(self):
        """Determine the best option to play."""
        self.e = len(me.hand.cards)
        for card in table.cards:
            for unknown in self.unknowns:
                if str(card) == str(unknown):
                    self.unknowns.remove(unknown)
                    break
        options = get_options(self.hand)
        if options == []:
            self.skip()
        else:
            p = 1.0
            toPlay = None
            for option in options:
                mytuple = analyze(option, self.unknowns, self.e)
                print mytuple
                score = mytuple[1] * mytuple[2]
                print score
                if score < p:
                    p = score
                    toPlay = option
                elif score == p:
                    if toPlay is None:
                        toPlay=option
                    elif option[len(option) - 1].pip < toPlay[len(toPlay) - 1].pip:
                        toPlay = option
            self.play(toPlay)


class Table(object):
    def __init__(self, money=100):
        self.players = [Player(money, "Ceasar"),AI(money, "Computer")]
        self.deck = Deck(new_deck())
        self.deck.shuffle()
        self.cards = []

    def start(self):
        """Start a game of 13."""
        for x in range(0, 2):
            self.deck.deal(self.players[x].hand)
            self.players[x].hand.sort()
        self.players[1].calibrate()
        display()

    def validate(self, cards):
        """Check if the cards played are valid."""
        if len(self.cards) == 0:
            return True
        else:
            if len(self.cards) == len(cards):
                highpip = self.cards[len(self.cards)-1].pip
                if cards[len(cards) - 1].pip > highpip:
                    if len(cards) == 1:
                        return True
                    elif is_tuple(cards) and is_tuple(self.cards):
                        return True
                    elif is_straight(cards) and is_straight(self.cards):
                        return True
        return False

    def __str__(self):
        toprint = ""
        for index, card in enumerate(self.cards):
            toprint += str(index + 1) + ": " + str(card)+"\n"
        if (toprint == ""):
            toprint = "The table is empty. "
        return toprint


table = Table()
me = table.players[0]
ai = table.players[1]
