from django.urls import path 

from . import views

urlpatterns = [
  path("new/", views.article_new, name="article_new"),
  path("<int:article_id>/", views.article_detail, name="article_detail"),
  path("<int:article_id>/edit/", views.article_edit, name="article_edit"),
  path("<int:article_id>/comments/", views.comment_new, name="comment_new"),
]