from django.urls import path
from .import views


urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contactpage/',views.contactpage,name='contactpage'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
   path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('search/', views.searchbook, name='searchbook'),
]

