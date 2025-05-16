from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .logic.war_logic import initialize_war_game, play_turn, Card
from .logic.poker_logic import initialize_poker_game, result_checker
from .forms import MyUserCreationForm
import json


def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method=="POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "An error occured during registration.")

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def victory(request):
    context = {}
    return render(request, 'base/victory.html', context)

def defeat(request):
    context = {}
    return render(request, 'base/defeat.html', context)

def war(request):
    if request.method == "GET":
        if 'my_hand_war' not in request.session or 'enemy_hand_war' not in request.session:
            my_hand, enemy_hand = initialize_war_game()
            
            request.session['my_hand_war'] = [(card.rank, card.suit) for card in my_hand]
            request.session['enemy_hand_war'] = [(card.rank, card.suit) for card in enemy_hand]

        my_hand = [Card(rank, suit) for rank, suit in request.session['my_hand_war']]
        enemy_hand = [Card(rank, suit) for rank, suit in request.session['enemy_hand_war']]

        war_status = False
        if my_hand[0].rank == enemy_hand[0].rank:
            war_status = True  

        context = {'my_hand': len(my_hand), 'enemy_hand': len(enemy_hand), 'war_status': war_status,
                'my_first': {'rank': my_hand[0].rank, 'suit': my_hand[0].suit}, 
                'enemy_first': {'rank': enemy_hand[0].rank, 'suit': enemy_hand[0].suit},
                'my_card_image': f'images/cards/{my_hand[0].rank}{my_hand[0].suit}.png',
                'enemy_card_image': f'images/cards/{enemy_hand[0].rank}{enemy_hand[0].suit}.png'}
        return render(request, 'base/war.html', context)

    elif request.method == "PUT":
        my_hand = [Card(rank, suit) for rank, suit in request.session['my_hand_war']]
        enemy_hand = [Card(rank, suit) for rank, suit in request.session['enemy_hand_war']]

        result, my_hand, enemy_hand = play_turn(my_hand, enemy_hand)
        if result == 'victory':
            reset_war(request)
            return JsonResponse({'status': 'redirect', 'url': '/victory'})
        if result == 'defeat':
            reset_war(request)
            return JsonResponse({'status': 'redirect', 'url': '/defeat'})

        request.session['my_hand_war'] = [(card.rank, card.suit) for card in my_hand]
        request.session['enemy_hand_war'] = [(card.rank, card.suit) for card in enemy_hand]

        war_status = False
        if my_hand[0].rank == enemy_hand[0].rank:
            war_status = True  

        context = {'my_hand': len(my_hand), 'enemy_hand': len(enemy_hand), 'war_status': war_status,
                'my_first': {'rank': my_hand[0].rank, 'suit': my_hand[0].suit}, 
                'enemy_first': {'rank': enemy_hand[0].rank, 'suit': enemy_hand[0].suit},
                'my_card_image': f'images/cards/{my_hand[0].rank}{my_hand[0].suit}.png',
                'enemy_card_image': f'images/cards/{enemy_hand[0].rank}{enemy_hand[0].suit}.png'}
        return JsonResponse(context)

def reset_war(request):
    if 'my_hand_war' in request.session:
        del request.session['my_hand_war']
    if 'enemy_hand_war' in request.session:
        del request.session['enemy_hand_war']
    return redirect('war')

def poker(request):
    if request.method == "GET":
        my_hand, enemy_hand, flop, turn, river, all_my_cards, all_enemy_cards = initialize_poker_game()
        my_comb, enemy_comb, my_result, enemy_result = result_checker(all_my_cards, all_enemy_cards)
        card1, card2, card3, card4, card5 = flop[0], flop[1], flop[2], turn, river
        my_card1, my_card2 = my_hand[0], my_hand[1]
        enemy_card1, enemy_card2 = enemy_hand[0], enemy_hand[1]
        counter = 0
        my_balance = 5000
        enemy_balance = 5000
        total_pot = 0
        max_raise = min(my_balance, enemy_balance)
               
        request.session['my_hand'] = [(card.rank, card.suit) for card in my_hand]
        request.session['enemy_hand'] = [(card.rank, card.suit) for card in enemy_hand]
        request.session['flop'] = [(card.rank, card.suit) for card in flop]
        request.session['turn'] = [(turn.rank, turn.suit)]
        request.session['river'] = [(river.rank, river.suit)]
        request.session['my_comb'] = my_comb
        request.session['enemy_comb'] = enemy_comb
        request.session['my_result'] = my_result
        request.session['enemy_result'] = enemy_result
        request.session['counter'] = counter
        request.session['my_balance'] = my_balance
        request.session['enemy_balance'] = enemy_balance
        request.session['total_pot'] = total_pot
        request.session['max_raise'] = max_raise
        request.session['all_my_cards'] = [(card.rank, card.suit) for card in all_my_cards]
        request.session['all_enemy_cards'] = [(card.rank, card.suit) for card in all_enemy_cards]

        context = {'my_hand': my_hand, 'enemy_hand': enemy_hand, 'counter': counter, 'total_pot': total_pot,
                'my_balance': my_balance, 'enemy_balance': enemy_balance, 'max_raise': max_raise,
                'card1_image': f'images/cards/{card1.rank}{card1.suit}.png',
                'card2_image': f'images/cards/{card2.rank}{card2.suit}.png',
                'card3_image': f'images/cards/{card3.rank}{card3.suit}.png',
                'card4_image': f'images/cards/{card4.rank}{card4.suit}.png',
                'card5_image': f'images/cards/{card5.rank}{card5.suit}.png',
                'my_card1_image': f'images/cards/{my_card1.rank}{my_card1.suit}.png',
                'my_card2_image': f'images/cards/{my_card2.rank}{my_card2.suit}.png',                
                'enemy_card1_image': f'images/cards/{enemy_card1.rank}{enemy_card1.suit}.png',
                'enemy_card2_image': f'images/cards/{enemy_card2.rank}{enemy_card2.suit}.png',
                'my_comb': my_comb, 'enemy_comb': enemy_comb, 'my_result': my_result, 'enemy_result': enemy_result}
        return render(request, 'base/poker.html', context)    
 
    elif request.method == "PUT":
        if request.body:
            data = json.loads(request.body)
            if 'my_balance' in data:
                request.session['my_balance'] = data['my_balance']
            if 'enemy_balance' in data:
                request.session['enemy_balance'] = data['enemy_balance']
            if 'max_raise' in data:
                request.session['max_raise'] = data['max_raise']
            if 'total_pot' in data:
                request.session['total_pot'] = data['total_pot']

        my_balance = request.session.get('my_balance')
        enemy_balance = request.session.get('enemy_balance')
        my_result = request.session.get('my_result')
        enemy_result = request.session.get('enemy_result')    
      
        my_hand = [Card(rank, suit) for rank, suit in request.session['my_hand']]
        enemy_hand = [Card(rank, suit) for rank, suit in request.session['enemy_hand']]
        card1, card2, card3 = [Card(rank, suit) for rank, suit in request.session['flop']]
        card4 = [Card(rank, suit) for rank, suit in request.session['turn']][0]
        card5 = [Card(rank, suit) for rank, suit in request.session['river']][0]
        enemy_card1, enemy_card2 = [Card(rank, suit) for rank, suit in request.session['enemy_hand']]
        all_my_cards = [Card(rank, suit) for rank, suit in request.session['all_my_cards']]
        all_enemy_cards = [Card(rank, suit) for rank, suit in request.session['all_enemy_cards']]
       
        counter = request.session.get('counter')
        max_raise = request.session.get('max_raise')
        total_pot = request.session.get('total_pot')
        my_comb = request.session.get('my_comb')
        enemy_comb = request.session.get('enemy_comb')
        
        counter += 1
        request.session['counter'] = counter

        context = {'my_balance': my_balance, 'enemy_balance': enemy_balance, 'max_raise': max_raise, 'total_pot': total_pot,
                'card1_image': f'images/cards/{card1.rank}{card1.suit}.png', 'counter': counter,
                'card2_image': f'images/cards/{card2.rank}{card2.suit}.png',
                'card3_image': f'images/cards/{card3.rank}{card3.suit}.png',
                'card4_image': f'images/cards/{card4.rank}{card4.suit}.png',
                'card5_image': f'images/cards/{card5.rank}{card5.suit}.png',
                'my_card1_image': f'images/cards/{my_hand[0].rank}{my_hand[0].suit}.png',
                'my_card2_image': f'images/cards/{my_hand[1].rank}{my_hand[1].suit}.png',                
                'enemy_card1_image': f'images/cards/{enemy_hand[0].rank}{enemy_hand[0].suit}.png',
                'enemy_card2_image': f'images/cards/{enemy_hand[1].rank}{enemy_hand[1].suit}.png',
                'my_comb': my_comb, 'enemy_comb': enemy_comb, 'my_result': my_result, 'enemy_result': enemy_result}
        return JsonResponse(context)
    
def restart_poker_game(request): 
    my_hand, enemy_hand, flop, turn, river, all_my_cards, all_enemy_cards = initialize_poker_game()
    my_comb, enemy_comb, my_result, enemy_result = result_checker(all_my_cards, all_enemy_cards)
    counter = 0
    total_pot = 0
    my_balance = request.session.get('my_balance')
    enemy_balance = request.session.get('enemy_balance')
    max_raise = min(my_balance, enemy_balance)

    request.session['my_hand'] = [(card.rank, card.suit) for card in my_hand]
    request.session['enemy_hand'] = [(card.rank, card.suit) for card in enemy_hand]
    request.session['flop'] = [(card.rank, card.suit) for card in flop]
    request.session['turn'] = [(turn.rank, turn.suit)]
    request.session['river'] = [(river.rank, river.suit)]
    request.session['my_comb'] = my_comb
    request.session['enemy_comb'] = enemy_comb
    request.session['my_result'] = my_result
    request.session['enemy_result'] = enemy_result
    request.session['counter'] = counter
    request.session['total_pot'] = total_pot
    request.session['all_my_cards'] = [(card.rank, card.suit) for card in all_my_cards]
    request.session['all_enemy_cards'] = [(card.rank, card.suit) for card in all_enemy_cards]

    context = {
        'card1_image': f'images/cards/{flop[0].rank}{flop[0].suit}.png',
        'card2_image': f'images/cards/{flop[1].rank}{flop[1].suit}.png',
        'card3_image': f'images/cards/{flop[2].rank}{flop[2].suit}.png',
        'card4_image': f'images/cards/{turn.rank}{turn.suit}.png',
        'card5_image': f'images/cards/{river.rank}{river.suit}.png',
        'my_card1_image': f'images/cards/{my_hand[0].rank}{my_hand[0].suit}.png',
        'my_card2_image': f'images/cards/{my_hand[1].rank}{my_hand[1].suit}.png',            
        'enemy_card1_image': f'images/cards/{enemy_hand[0].rank}{enemy_hand[0].suit}.png',
        'enemy_card2_image': f'images/cards/{enemy_hand[1].rank}{enemy_hand[1].suit}.png',
        'my_balance': my_balance, 'enemy_balance': enemy_balance, 'max_raise': max_raise, 'total_pot': total_pot
    }
    return JsonResponse(context)