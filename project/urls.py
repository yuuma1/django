from django.urls import path, include
import snsapp
from django.contrib import admin, auth
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('snsapp.urls')),
    path('thread/', include('thread.urls')),
    path('api/', include('api.urls')),
] 

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

