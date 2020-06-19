from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('EAS/', include('EAS.urls')),
    path('admin/', admin.site.urls),
]