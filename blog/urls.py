from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='post-index'),
    path('create/', create_post, name='post-create'),
    path('detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('create-comment/<int:pk>/', create_comment, name='create-comment'),
    path('search/', search, name='search'),
    path('signup/',signup, name='signup'),
    path('signin/',signin, name='signin'),
    path('signout/',signout, name='signout'),
    path('edit-profile/',edit_profile, name='edit-profile'),
    path('like/<int:pk>/',like, name='like'),
    path('liked-posts/',liked_posts, name='liked-posts'),
    path('own-posts/',UserPostsView.as_view(), name='own-posts'),
    path('<str:category>/', CategoryView.as_view(), name='category-view'),
    
]

