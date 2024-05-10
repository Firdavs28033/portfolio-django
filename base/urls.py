from django.urls import path

from .views import home, posts, post, profile, create_post, update_post, \
    delete_post, sendEmail, loginPage
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('post/<slug:slug>/', post, name='post'),
    path('profile/', profile, name='profile'),

    #CRUD urls
    path('create_post/', create_post, name='create_post'),
    path('update_post/<slug:slug>/', update_post, name='update_post'),
    path('delete_post/<slug:slug>/', delete_post, name='delete_post'),

    path('send_email/', sendEmail, name="send_email"),
    # Authenticate
    path('login/', loginPage, name="login"),
    path('register/', views.registerPage, name="register" ),
    path('logout/', views.logout1, name="logout"),

    # Profile
    path('accounts/', views.userAccount, name='account'),
    path('update_profile/', views.updateProfile, name='update_profile'),

]