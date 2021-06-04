from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('users.urls', 'users'), namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include(('recipes.urls', 'recipes'), namespace='recipes')),
]
