# project/urls.py

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path('', show_about, name="about"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile', ShowProfileHomeView.as_view(),name="profile_home"),
    path('profile/create_pm', CreatePersonalMessageView.as_view(),name="create_pm"),
    path('profile/search_new_friends', SearchNewFriendsListView.as_view(), name="search_new_friends"),
    path('profile/add_friend/<int:other_pk>', CreateFriendView.as_view(), name="add_friend"),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
]