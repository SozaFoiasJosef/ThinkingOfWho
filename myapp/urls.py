from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('joingame/', views.joingame, name='joingame'),
    path('creategame/', views.creategame, name='creategame'),
    path('game/<uuid:room_id>/', views.game,name='game'),
    path('gamelistall/', views.gamelistall, name='gamelistall'),
    path('gamelist/<str:room_name>/', views.gamelist, name='gamelist'),
    path('tos/', views.tos,name='tos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)