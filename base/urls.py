from django.urls import path

from .views import home, posts, post, profile, create_post, update_post, delete_post, sendEmail

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

]