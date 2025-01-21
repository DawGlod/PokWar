import random

class Card:
    ranks = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']
    suits = ['H', 'D', 'C', 'S']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.image = self.get_image_path()


    def get_image_path(self):
        return f"images/cards/{self.rank}{self.suit}.png"
    

    def __repr__(self):
        return f"{self.rank}{self.suit}"
    
    
    def rank_value(self):
        return Card.ranks.index(self.rank)
    
    
    @staticmethod
    def rank_value_nocard(rank):
        return Card.ranks.index(rank)
    

    def suit_value(self):
        return Card.suits.index(self.suit)
    
    
    @staticmethod
    def suit_value_nocard(suit):
        return Card.suits.index(suit)
    

def initialize_war_game():
    deck = [Card(rank, suit) for suit in Card.suits for rank in Card.ranks]
    random.shuffle(deck)

    half_deck_size = len(deck) // 2
    my_hand = deck[:half_deck_size]
    enemy_hand = deck[half_deck_size:]

    return my_hand, enemy_hand

def play_turn(my_hand, enemy_hand):
    result = f'{my_hand[0]} vs {enemy_hand[0]}'

    if Card.ranks.index(my_hand[0].rank) < Card.ranks.index(enemy_hand[0].rank):
        result += " - You Won!"
        my_hand.append(my_hand.pop(0))
        my_hand.append(enemy_hand.pop(0))
    elif Card.ranks.index(my_hand[0].rank) == Card.ranks.index(enemy_hand[0].rank):
        result, my_hand, enemy_hand = war(my_hand, enemy_hand)
    else:
        result += " - You Lost!"
        enemy_hand.append(enemy_hand.pop(0))
        enemy_hand.append(my_hand.pop(0))

    if len(enemy_hand) == 0:
        result = "victory"
        return result, my_hand, enemy_hand
    if len(my_hand) == 0:
        result = "defeat"
        return result, my_hand, enemy_hand

    return result, my_hand, enemy_hand

def war(my_hand, enemy_hand):
    counter = 2
    while True:
        if len(my_hand) >= (counter + 1) and len(enemy_hand) >= (counter + 1):
            result = f'{my_hand[0]} vs {enemy_hand[0]} - WAR'
            if Card.ranks.index(my_hand[counter].rank) < Card.ranks.index(enemy_hand[counter].rank):
                result += " - You Won!"
                for n in range(counter + 1):
                    my_hand.append(my_hand.pop(0))
                    my_hand.append(enemy_hand.pop(0))
                return result, my_hand, enemy_hand
            elif Card.ranks.index(my_hand[counter].rank) == Card.ranks.index(enemy_hand[counter].rank):
                result += " - WAR!"
                counter += 2
                continue
            else:
                result += " - You Lost!"
                for n in range(counter + 1):
                    enemy_hand.append(enemy_hand.pop(0))
                    enemy_hand.append(my_hand.pop(0))
                return result, my_hand, enemy_hand
        else:
            if len(my_hand) > len(enemy_hand):
                result = 'WIN'
                enemy_hand.clear()
            else:
                result = 'LOSE'
                my_hand.clear()
            return result, my_hand, enemy_hand

        