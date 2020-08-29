from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('add_fav/<int:book_id>', views.add_fav),
    path('un_favorite/<int:book_id>', views.un_favorite),
    path('books/<int:book_id>', views.one_book),
    path('update/<int:book_id>', views.update),
    path('delete_book/<int:book_id>', views.delete_book),
    path('favorites', views.favorites)
]