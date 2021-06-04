from django.urls import include, path

from . import views
from recipes.views import Recipes

urlpatterns = [
    path('registration/',
         views.Register.as_view(),
         name='registration'),
    path('login/',
         views.Login.as_view(),
         name='login'),
]
