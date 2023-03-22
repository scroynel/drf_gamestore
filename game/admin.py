from django.contrib import admin

from .models import Game, Genre, Developer, Review, Rating, RatingStar


admin.site.register(Game)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
admin.site.register(Review, ReviewAdmin)

admin.site.register(Rating)

class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
admin.site.register(RatingStar, RatingStarAdmin)


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Genre, GenreAdmin)


class DeveloperAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Developer, DeveloperAdmin)