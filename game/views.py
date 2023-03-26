from django.shortcuts import render
from django.db import models

from .serializers import GamesListSerializer, GamesDetailSerializer, ReviewCreateSerializer, RatingSerializer, GamesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .models import Game
from .services import GamesFilter

# class GamesList(APIView):
#     filter_beckends = (DjangoFilterBackend,)
#     filterset_class = GamesFilter

#     def get(self, request):
#         if request.user.is_authenticated:
#             games = Game.objects.all().annotate(
#                 rating_user = models.Count('ratings', filter=models.Q(ratings__user = request.user))
#             ).annotate(
#                 middle_star = models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#             )
#             serializer = GamesListSerializer(games, many=True)
#         else:
#             games = Game.objects.all()
#             serializer = GamesSerializer(games, many=True)
#         return Response(serializer.data)

class GamesList(viewsets.ReadOnlyModelViewSet):
    filter_beckends = (DjangoFilterBackend,)
    filterset_class = GamesFilter


    def get_queryset(self):
        if self.request.user.is_authenticated:
            games = Game.objects.all().annotate(
                rating_user = models.Count('ratings', filter=models.Q(ratings__user = self.request.user))
            ).annotate(
                middle_star = models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            )
        else:
            games = Game.objects.all()
    
        return games


    def get_serializer_class(self):
        if self.action == 'list':
            return GamesListSerializer
        elif self.action == 'retrieve':
            return GamesDetailSerializer



# class GamesDetail(APIView):
#     def get(self, request, pk):
#         game = Game.objects.get(pk=pk)
#         serializer = GamesDetailSerializer(game)
#         return Response(serializer.data)


class ReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=201)
    
# class AddStarRatingView(APIView):
#     def post(self, request): 
#         serializer = RatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(status=201)
#         else:
#             return Response(status=400)
        
class AddStarRatingView(generics.CreateAPIView):
    
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    # при сохранении нам нужно указывать user
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        

       
    