from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
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

    def __str__(self):
        return self.name + ', ' + self.unit


class EatingTimes(models.Model):
    title = models.CharField(
        unique=True,
        max_length=30,
        verbose_name='Название',
    )
    slug = models.CharField(
        max_length=30,
        blank=True,
    )
    color = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        verbose_name='Цвет',
    )

    class Meta:
        verbose_name = 'Время приема пищи'
        verbose_name_plural = 'Время приема пищи'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(
        max_length=30,
        verbose_name='Название',
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
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name='Картинка',
    )
    tag = models.ManyToManyField(
        EatingTimes,
        blank=True,
        null=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Минуты',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient',),
        verbose_name='Ингредиент',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredient',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_recipe',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Ингредиент',
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
