from django.urls import path
from . import views


urlpatterns = [
   
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('item/create', views.createItem),
    path('uploadItem', views.uploadItem),
    path('item/<int:itemId>', views.itemInfo),
    path('addFav/<int:itemId>', views.addFav),
    path('remove/<int:itemId>', views.remove),
    path('delete/<int:itemId>', views.delete),
]
