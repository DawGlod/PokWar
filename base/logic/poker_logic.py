import random
from .war_logic import Card

def initialize_poker_game():
    deck = [Card(rank, suit) for suit in Card.suits for rank in Card.ranks]
    random.shuffle(deck)

    my_comb = []
    enemy_comb = []
    my_hand = deck[:2]
    enemy_hand=deck[2:4]
    flop = deck[4:7]
    turn = deck[8]
    river = deck[9]

    my_comb += my_hand
    my_comb += flop
    my_comb.append(turn)
    my_comb.append(river)
    my_comb = sorted(my_comb, key=lambda card: (card.rank_value(), card.suit_value()))

    enemy_comb += enemy_hand
    enemy_comb += flop
    enemy_comb.append(turn)
    enemy_comb.append(river)
    enemy_comb = sorted(enemy_comb, key=lambda card: (card.rank_value(), card.suit_value()))

    return my_hand, enemy_hand, flop, turn, river, my_comb, enemy_comb

combs_ranking = {
    'Royal Flush': 1,
    'Straight Flush': 2,
    'Four of a Kind': 3,
    'Full House': 4,
    'Flush': 5,
    'Straight': 6,
    'Three of a Kind': 7,
    'Two Pair': 8,
    'Pair': 9,
    'High Card': 10
}


def royal_flush_checker(comb):
    royal_flush_ranks = {'A', 'K', 'Q', 'J', '10'}
    suits_count={}
    for card in comb:
        rank = card.rank
        suit = card.suit

        if suit not in suits_count:
            suits_count[suit] = []
            
        suits_count[suit].append(rank)

    highest_rank = 'A'
    
    for suit, ranks in suits_count.items():
        if royal_flush_ranks.issubset(ranks):
            return "Royal Flush", highest_rank


def straight_flush_checker(comb):
    suits_count={}
    for card in comb:
        rank = card.rank
        suit = card.suit

        if suit not in suits_count:
            suits_count[suit] = []
            
        suits_count[suit].append(rank)
    
    for suit, ranks in suits_count.items():
        if len(ranks) >= 5:
            for i in range(len(ranks) - 4):                
                if Card.rank_value_nocard(ranks[i + 4]) - Card.rank_value_nocard(ranks[i]) == 4:
                    highest_rank = ranks[i]
                    return "Straight Flush", highest_rank


def four_of_a_kind_checker(comb):
    ranks_count={}
    for card in comb:
        rank = card.rank

        if rank not in ranks_count:
            ranks_count[rank] = 1
        else:
            ranks_count[rank] += 1

    for rank, count in ranks_count.items():
        if count == 4:
            return "Four of a Kind", rank


def full_house_checker(comb):
    ranks_count={}
    for card in comb:
        rank = card.rank

        if rank not in ranks_count:
            ranks_count[rank] = 1
        else:
            ranks_count[rank] += 1

    three_rank = None
    pair_rank = None

    for rank, counter in ranks_count.items():       
        if counter == 3 and three_rank is None:
            three_rank = rank
            continue
        if counter == 2 and pair_rank is None:
            pair_rank = rank
    if three_rank and pair_rank:
        return "Full House", three_rank, pair_rank
        

def flush_checker(comb):
    suits_count={}
    for card in comb:
        rank = card.rank
        suit = card.suit

        if suit not in suits_count:
            suits_count[suit] = []
        suits_count[suit].append(rank)
    
    for suit, ranks in suits_count.items():
        if len(ranks) >= 5:
            highest_rank = ranks[0]
            return "Flush", highest_rank


def straight_checker(comb):
    ranks_count = []
    for card in comb:
        rank = card.rank

        if rank not in ranks_count:
            ranks_count.append(rank)
    
    for i in range(len(ranks_count) - 4):
        if Card.rank_value_nocard(ranks_count[i+4]) - Card.rank_value_nocard(ranks_count[i]) == 4:
            highest_card = ranks_count[i]
            return "Straight", highest_card


def three_of_a_kind_checker(comb):
    ranks_count={}
    for card in comb:
        rank = card.rank

        if rank not in ranks_count:
            ranks_count[rank] = 1
        else:
            ranks_count[rank] += 1

    for rank, count in ranks_count.items():
        if count == 3:
            return "Three of a Kind", rank


def two_pair_checker(comb):
    ranks_count={}
    for card in comb:
        rank = card.rank

        if rank not in ranks_count:
            ranks_count[rank] = 1
        else:
            ranks_count[rank] += 1

    highest_rank = None

    for rank, count in ranks_count.items():       
        if count == 2 and highest_rank is None:
            highest_rank = rank
            continue
        if count == 2 and highest_rank is not None:
            second_highest_rank = rank
            return "Two Pair", highest_rank, second_highest_rank


def pair_checker(comb):
    ranks_count={}
    for card in comb:
        rank = card.rank

        if rank not in ranks_count:
            ranks_count[rank] = 1
        else:
            ranks_count[rank] += 1

    for rank, count in ranks_count.items():
        if count == 2:
            return "Pair", rank


def high_card_checker(comb):
    ranks_count = []
    for card in comb:
        rank = card.rank

        if rank not in ranks_count:
            ranks_count.append(rank)

    highest_rank = ranks_count[0]
    return "High Card", highest_rank


def comb_checker(comb):
    result = royal_flush_checker(comb)
    if result:
        return result

    result = straight_flush_checker(comb)
    if result:
        return result

    result = four_of_a_kind_checker(comb)
    if result:
        return result

    result = full_house_checker(comb)
    if result:
        return result

    result = flush_checker(comb)
    if result:
        return result

    result = straight_checker(comb)
    if result:
        return result

    result = three_of_a_kind_checker(comb)
    if result:
        return result

    result = two_pair_checker(comb)
    if result:
        return result

    result = pair_checker(comb)
    if result:
        return result

    return high_card_checker(comb)


def result_checker(my_cards, enemy_cards):
    my_comb = comb_checker(my_cards)[0]
    enemy_comb = comb_checker(enemy_cards)[0]
    if combs_ranking[my_comb] < combs_ranking[enemy_comb]:
        my_result = 'WIN'
        enemy_result = 'LOSE'
    elif combs_ranking[my_comb] > combs_ranking[enemy_comb]:
        my_result = 'LOSE'
        enemy_result = 'WIN'
    else:
        my_highest_rank = comb_checker(my_cards)[1]
        enemy_highest_rank = comb_checker(enemy_cards)[1]
        if (my_comb == 'Full House' and enemy_comb == 'Full House') or (my_comb == 'Two Pair' and enemy_comb == 'Two Pair'):
            if Card.rank_value_nocard(my_highest_rank) < Card.rank_value_nocard(enemy_highest_rank):
                my_result = 'WIN'
                enemy_result = 'LOSE'
            elif Card.rank_value_nocard(my_highest_rank) > Card.rank_value_nocard(enemy_highest_rank):
                my_result = 'LOSE'
                enemy_result = 'WIN'
            else:
                my_second_highest_rank = comb_checker(my_cards)[2]
                enemy_second_highest_rank = comb_checker(enemy_cards)[2]
                if Card.rank_value_nocard(my_second_highest_rank) < Card.rank_value_nocard(enemy_second_highest_rank):
                    my_result = 'WIN'
                    enemy_result = 'LOSE'
                elif Card.rank_value_nocard(my_second_highest_rank) > Card.rank_value_nocard(enemy_second_highest_rank):
                    my_result = 'LOSE'
                    enemy_result = 'WIN'
                else:
                    my_result = 'DRAW'
                    enemy_result = 'DRAW'
        else:
            if Card.rank_value_nocard(my_highest_rank) < Card.rank_value_nocard(enemy_highest_rank):
                my_result = 'WIN'
                enemy_result = 'LOSE'
            elif Card.rank_value_nocard(my_highest_rank) > Card.rank_value_nocard(enemy_highest_rank):
                my_result = 'LOSE'
                enemy_result = 'WIN'
            else:
                my_result = 'DRAW'
                enemy_result = 'DRAW'

    return my_comb, enemy_comb, my_result, enemy_result