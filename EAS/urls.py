from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in', views.sign_in),
    path('sign_up', views.sign_up),
    path('display', views.display),
    path('pick', views.pick),
    path('delete', views.delete),
]