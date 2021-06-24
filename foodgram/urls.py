from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from recipes.views import PageNotFoundView

handler404 = PageNotFoundView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('users.urls', 'users'), namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include(('recipes.urls', 'recipes'), namespace='recipes')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
