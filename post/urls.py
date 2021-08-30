from django.urls import path
from . views import *

# app_name="blog"

urlpatterns = [
    path('',post_index,name="index"),
    path('post/create',PostCreateView.as_view(),name="create"),
    path('post/detail/<slug:slug>',post_detail,name="detail"),
    path('post/update/<slug:slug>',PostUpdateView.as_view(),name="update"),
    path('post/delete/<slug:slug>',PostDeleteView.as_view(),name="delete"),
    path('like/<slug:slug>',post_like, name="like_post"),
]
