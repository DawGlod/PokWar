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
    result = ""
    #I win
    if Card.ranks.index(my_hand[0].rank) < Card.ranks.index(enemy_hand[0].rank):
        my_hand.append(my_hand.pop(0))
        my_hand.append(enemy_hand.pop(0))
    #draw
    elif Card.ranks.index(my_hand[0].rank) == Card.ranks.index(enemy_hand[0].rank):
        my_hand, enemy_hand = war(my_hand, enemy_hand)
    #I lose
    else:
        enemy_hand.append(enemy_hand.pop(0))
        enemy_hand.append(my_hand.pop(0))

    result = "victory" if len(enemy_hand) == 0 else "defeat" if len(my_hand) == 0 else ""

    return result, my_hand, enemy_hand

def war(my_hand, enemy_hand):
    counter = 2
    while True:
        if len(my_hand) >= (counter + 1) and len(enemy_hand) >= (counter + 1):
            if Card.ranks.index(my_hand[counter].rank) < Card.ranks.index(enemy_hand[counter].rank):
                for _ in range(counter + 1):
                    my_hand.append(my_hand.pop(0))
                    my_hand.append(enemy_hand.pop(0))
                return my_hand, enemy_hand
            elif Card.ranks.index(my_hand[counter].rank) == Card.ranks.index(enemy_hand[counter].rank):
                counter += 2
                continue
            else:
                for _ in range(counter + 1):
                    enemy_hand.append(enemy_hand.pop(0))
                    enemy_hand.append(my_hand.pop(0))
                return my_hand, enemy_hand
        else:
            enemy_hand.clear() if len(my_hand) > len(enemy_hand) else my_hand.clear()
            
            return my_hand, enemy_hand

        