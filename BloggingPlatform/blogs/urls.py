from django.urls import path

from .views import *

urlpatterns=[
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('create-post/',createpost,name='create_post'),
    path('edit/<int:post_id>/', edit_blog_post, name='edit_blog_post'),
    path('delete/<int:post_id>/', delete_blog_post, name='delete_blog_post'),
    path('post-details/<int:post_id>',viewpost,name='post_detail'),
    path('<int:post_id>/comment/',add_comment, name='add_comment'),
    path('search/', search_blog_posts, name='search_blog_posts'),
    path('categories/', filter_categories, name='filter_categories'),
    path('tags/', filter_tags, name='filter_tags'),
    # Other URL patterns...

    #Left with Profile ... and Search and Filteration
]
