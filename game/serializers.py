from rest_framework import serializers

from .models import Game, Genre, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ['name', 'email', 'text', 'children']


class GameSerializer(serializers.ModelSerializer):
    developer = serializers.SlugRelatedField(slug_field='name', read_only=True)
    genres = GenresSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Game
        fields = '__all__'
    