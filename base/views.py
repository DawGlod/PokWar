from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .logic.war_logic import initialize_war_game, play_turn, Card
from .logic.poker_logic import initialize_poker_game, result_checker


def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def login(request):
    context = {}
    return render(request, 'base/login_register.html', context)

def register(request):
    context = {}
    return render(request, 'base/login_register.html', context)

def victory(request):
    context = {}
    return render(request, 'base/victory.html', context)

def defeat(request):
    context = {}
    return render(request, 'base/defeat.html', context)

def war(request):
    if 'my_hand' not in request.session or 'enemy_hand' not in request.session:
        my_hand, enemy_hand = initialize_war_game()
        request.session['my_hand'] = [(card.rank, card.suit) for card in my_hand]
        request.session['enemy_hand'] = [(card.rank, card.suit) for card in enemy_hand]
    
    my_hand = [Card(rank, suit) for rank, suit in request.session['my_hand']]
    enemy_hand = [Card(rank, suit) for rank, suit in request.session['enemy_hand']]

    if my_hand and enemy_hand:
        result, my_hand, enemy_hand = play_turn(my_hand, enemy_hand)
        if result == 'victory':
            reset_war(request)
            return HttpResponseRedirect('/victory')
        if result == 'defeat':
            reset_war(request)
            return HttpResponseRedirect('/defeat')

        request.session['my_hand'] = [(card.rank, card.suit) for card in my_hand]
        request.session['enemy_hand'] = [(card.rank, card.suit) for card in enemy_hand]

    context = {'my_hand': len(my_hand), 'enemy_hand': len(enemy_hand), 'my_first': my_hand[0], 'enemy_first': enemy_hand[0]}
    return render(request, 'base/war.html', context)

def reset_war(request):
    if 'my_hand' in request.session:
        del request.session['my_hand']
    if 'enemy_hand' in request.session:
        del request.session['enemy_hand']
    if 'results' in request.session:
        del request.session['results']
    return redirect('war')

def poker(request):
    my_hand, enemy_hand, flop, turn, river, all_my_cards, all_enemy_cards = initialize_poker_game()
    my_comb, enemy_comb, my_result, enemy_result = result_checker(all_my_cards, all_enemy_cards)
    context = {'my_hand': my_hand, 'enemy_hand': enemy_hand, 'flop': flop, 'turn': turn, 'river': river, 
               'my_comb': my_comb, 'enemy_comb': enemy_comb, 'my_result': my_result, 'enemy_result': enemy_result}
    return render(request, 'base/poker.html', context)