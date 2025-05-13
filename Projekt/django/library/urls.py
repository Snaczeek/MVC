from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_create, name='book_create'),
    path('edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('add/authors', views.author_create, name='author_create'),
    path('borrow/<int:pk>', views.borrow_book, name='borrow_book'),
    path('my-borrows/', views.my_borrows, name='my_borrows'),
    path('return/<int:pk>/', views.return_book, name='return_book'),

    # auth
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
]
