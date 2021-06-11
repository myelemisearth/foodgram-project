from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название',
    )
    unit = models.CharField(
        max_length=30,
        verbose_name='Единица измерения',
    )
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class EatingTimes(models.Model):
    CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    )
    choice = models.CharField(
        unique=True,
        choices=CHOICES,
        max_length=30,
    )
    
    def __str__(self):
        return self.choice


class Recipe(models.Model):
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
    tag = models.ManyToManyField(
        EatingTimes,
        related_name='tag',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='В минутах',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ingredients',
        through_fields=('recipe', 'ingredient',),
        verbose_name='Ингредиент',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient',
        on_delete=models.DO_NOTHING,
        verbose_name='Ингредиент',
    )
