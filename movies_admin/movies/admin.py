from django.contrib import admin

from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkinline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = [
        GenreFilmworkInline,
        PersonFilmworkinline,
    ]
    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date',
                    'rating', 'created', 'modified',
                    )
    # Фильтрация в списке
    list_filter = ('type',)
    # Поиск по полям
    search_fields = ('title', 'description',
                     'creation_date', 'rating',
                     )
