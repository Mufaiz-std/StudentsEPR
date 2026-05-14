from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('doLogin/', views.do_login, name='do_login'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('profile/', views.profile_view, name='profile_view'),
]
