from . import views
from django.urls import path
from .views import AddNewUser, login_test, logout


urlpatterns = [
    path('register', AddNewUser.as_view(), name='register'),
    path('login', login_test, name='login'),
    path('logout', logout, name='logout'),
]
