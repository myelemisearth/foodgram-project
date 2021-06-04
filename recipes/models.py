from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
    )
    count = models.IntegerField(
        verbose_name='Количество',
    )
    unit = models.CharField(
        max_length=30,
        verbose_name='Единицы измерения',
    )
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    
class Recipe(models.Model):
    EATING_TIMES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]
    title = models.CharField(
        max_length=30,
        verbose_name='Название',
    )
    slug = models.SlugField(
        unique=True,
        max_length=30,
        verbose_name='Метка',
    )
    description = models.TextField(
        verbose_name='Текстовое описание',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='Картинка',
    )
    tag = models.CharField(
        max_length=30,
        choices=EATING_TIMES,
        blank=True,
        null=True,
        verbose_name='Тег',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.DO_NOTHING,
        verbose_name='Ингредиенты',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
