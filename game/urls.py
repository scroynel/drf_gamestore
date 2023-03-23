from django.urls import path

from .views import GamesList, GamesDetail, ReviewCreateView, AddStarRatingView
from .yasg import urlpatterns as dir_urls

urlpatterns = [
    path('games', GamesList.as_view(), name='games'),
    path('games/<int:pk>', GamesDetail.as_view(), name='games-detail'),
    path('review/', ReviewCreateView.as_view(), name= 'create-review'),
    path('rating/', AddStarRatingView.as_view(), name= 'create-rating')
]

urlpatterns += dir_urls