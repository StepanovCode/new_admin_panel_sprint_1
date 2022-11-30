import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('row_created'), auto_now_add=True)
    modified = models.DateTimeField(_('row_modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre_verbose_name')
        verbose_name_plural = _('genre_verbose_n_pl')

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name=_('genre_verbose_name')
    )
    created = models.DateTimeField(_('row_created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre_verbose_name')
        verbose_name_plural = _('genre_verbose_n_pl')

        indexes = [
            models.Index(fields=['film_work'],
                         name='genre_film_work_film_work_idx'),
            models.Index(fields=['genre'],
                         name='genre_film_work_genre_idx'),
        ]

    def __str__(self):
        return ''


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255, blank=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person_verbose_name')
        verbose_name_plural = _('person_verbose_n_pl')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        verbose_name=_('person_verbose_name')
    )
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(_('row_created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person_verbose_name')
        verbose_name_plural = _('person_verbose_n_pl')

        indexes = [
            models.Index(fields=['person'],
                         name='person_film_work_person_idx'),
            models.Index(fields=['film_work'],
                         name='person_film_work_film_work_idx'),
        ]

    def __str__(self):
        return ''


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeOfFilm(models.TextChoices):
        MOVIE = 'MOV', _('type_movie')
        TV_SHOW = 'TVS', _('tv_Show')
        SERIALS = 'SER', _('serials')

    title = models.CharField(_('title'), max_length=255, blank=True)
    description = models.TextField(_('description'))
    creation_date = models.DateTimeField(_('creation_date'), auto_now_add=True)
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )
    rating = models.FloatField(
        _('rating'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        default=5.0)

    type = models.CharField(
        _('type'),
        max_length=3,
        choices=TypeOfFilm.choices,
        default=TypeOfFilm.MOVIE
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmwork'
    )
    persons = models.ManyToManyField(
        Person,
        through='PersonFilmwork'
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film_work_verbose_name')
        verbose_name_plural = _('film_work_verbose_n_pl')

        indexes = [
            models.Index(fields=['title'], name='film_work_title_idx'),
        ]

    def __str__(self):
        return self.title
