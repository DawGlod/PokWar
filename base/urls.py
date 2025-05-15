from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('victory', views.victory, name='victory'),
    path('defeat/', views.defeat, name='defeat'),

    path('war/', views.war, name='war'),
    path('reset_war/', views.reset_war, name='reset_war'),
    
    path('poker/', views.poker, name='poker'),
    path('restart-poker/', views.restart_poker_game, name='restart_poker_game'),

]