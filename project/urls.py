from django.urls import path, include
import snsapp
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('snsapp.urls')),
    path('thread/', include('thread.urls')),
] 

