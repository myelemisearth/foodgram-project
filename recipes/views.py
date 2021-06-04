from typing import List
from django.shortcuts import render
from django.views.generic import ListView

from django.contrib.auth import get_user_model

User = get_user_model()

class Recipes(ListView):
    queryset = User.objects.all()


class Basket(ListView):
    pass
