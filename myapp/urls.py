from django.urls import path
from .views import (
    home_page,
    create_post_page,
    post_comment,
    search_posts,
    delete_post,
    edit_post,
    about,
    )
    
app_name = "myapp"

urlpatterns = [
  path("",home_page,name="home_page"),
  path("about",about,name="about"),
  path('create-post',create_post_page,name='create_post_page'),
  path("search",search_posts,name="search_posts"),
  path("<int:year>/<int:month>/<int:day>/<slug:post>",post_comment,name="post_comment"),
  path("<int:month>/<slug:post>/delete",delete_post,name="delete_post"),
  path("<int:day>/<slug:url>/edit",edit_post,name="edit_post"),
  
]