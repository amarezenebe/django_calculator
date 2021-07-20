from django.urls import path

from .views import (
    LogInView, SignUpView, LogOutView,
    ProfileView, Home, userHistory, ChangeProfileView, deleteHistory, deleteAllHistory)

app_name="accounts"

urlpatterns=[

    path('', LogInView.as_view(), name='login'),
    path('login/', LogInView.as_view(), name='login'),
    path('log-out/', LogOutView.as_view(), name='logout'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('home/', Home.as_view(), name='home'),
    path('userHistory/', userHistory.as_view(), name='history'),
    path('deleteHistory/<id>/', deleteHistory, name='delete_history'),
    path('deleteAllHistory/', deleteAllHistory, name='delete_all_history'),
    path('profile/', ProfileView, name='profile'),
    path('change_profile/', ChangeProfileView.as_view(), name='change_profile'),

]
