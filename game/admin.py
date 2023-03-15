from django.contrib import admin

from .models import Game, Genre, Developer, Review


admin.site.register(Game)
admin.site.register(Review)


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Genre, GenreAdmin)


class DeveloperAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Developer, DeveloperAdmin)