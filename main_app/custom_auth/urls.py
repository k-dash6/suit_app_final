from django.urls import path

from .views import started, register, user_login, user_logout

urlpatterns = [
    path('', started, name='started'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
