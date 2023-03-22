from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

LANGUAGES = [(1, 'English'), (2, 'Russian'), (3, 'Ukrainian')]


class Game(models.Model):
    name = models.CharField('Навание игры', max_length=255)
    description = models.TextField('Описание игры')
    language = models.IntegerField('Языки', choices=LANGUAGES, default=3)
    platform = models.CharField('Платформа', max_length=255)
    type = models.CharField('Тип', default='RePack', max_length=255)
    genres = models.ManyToManyField('Genre')
    developer = models.ForeignKey('Developer', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        return self.ratings.aggregate(Avg('star'))['star__avg']
    

class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=255)
    slug = models.SlugField('Genre slug')


    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField('Наименование разработчика', max_length=255)
    slug = models.SlugField('Developer slug')

    def __str__(self):
        return self.name
    

class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Комментарий', max_length=2000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='Игра', related_name='reviews')


    def __str__(self):
        return f'{self.name} --- {self.game}'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0, auto_created=0)

    def __str__(self):
        return f'{self.value}'
    
    class Meta:
        ordering = ["-value"]
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    star = models.ForeignKey('RatingStar', on_delete=models.CASCADE, related_name='star')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f'{self.star} --- {self.user} --- {self.game}'
    
    