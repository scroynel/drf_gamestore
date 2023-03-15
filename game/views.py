from django.shortcuts import render

from .serializers import GameSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game

class GameList(APIView):
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
