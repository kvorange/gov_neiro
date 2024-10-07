from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('system/', include('server.apps.system.urls')),
    path('api/', include('server.apps.neural.urls')),
]
