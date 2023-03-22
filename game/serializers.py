from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Game, Genre, Review, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ['name', 'email', 'text', 'children']

class GamesListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    class Meta:
        model = Game 
        fields = ['id', 'name', 'rating_user', 'middle_star']


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game 
        fields = ['id', 'name']



class RatingSerializer(serializers.ModelSerializer):
  
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Rating
        fields = ['user', 'star', 'game']


    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            user = validated_data.get('user', None),
            game = validated_data.get('game', None),
            defaults={'star': validated_data.get('star')} # эти данные мы будем обновлять
        )
        return rating

class GamesDetailSerializer(serializers.ModelSerializer):
    developer = serializers.SlugRelatedField(slug_field='name', read_only=True)
    genres = GenresSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    ratings = RatingSerializer(many=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating 

    class Meta:
        model = Game
        fields = '__all__'
        

    