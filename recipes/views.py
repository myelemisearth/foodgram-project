from typing import List
from django.shortcuts import render
from django.views.generic import ListView

from django.contrib.auth import get_user_model

from .models import Recipe

User = get_user_model()

class Recipes(ListView):
    queryset = Recipe.objects.all()
    template_name = 'main/index.html'


class Basket(ListView):
    pass
