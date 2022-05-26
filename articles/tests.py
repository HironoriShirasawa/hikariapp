from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.urls import resolve
from django.contrib.auth import get_user_model

from .models import Article
from .views import top, article_new, article_edit, article_detail

UserModel = get_user_model()

class TopPageRenderArticlesTest(TestCase):
  def setUp(self):
    self.user = UserModel.objects.create(
      username="test_user",
      email="test@example.com",
      password="topsecret",
    )
    self.article = Article.objects.create(
      title="title1",
      post="光市",
      created_by=self.user,
    )
  
  def test_should_return_article_title(self):
    request = RequestFactory().get("/")
    request.user = self.user
    response = top(request)
    self.assertContains(response, self.article.title)
  
  def test_should_return_username(self):
    request = RequestFactory().get("/")
    request.user = self.user
    response = top(request)
    self.assertContains(response, self.user.username)

class CreateArticleTest(TestCase):
  def setUp(self):
    self.user = UserModel.objects.create(
      username="test_user",
      email="test@example.com",
      password="topsecret",
    )
    self.client.force_login(self.user)
  
  def test_render_creation_form(self):
    response = self.client.get('/articles/new/')
    self.assertContains(response, "記事の投稿", status_code=200)
  
  def test_create_article(self):
    data = {'title': 'タイトル', 'post':'投稿内容'}
    self.client.post("/articles/new/", data)
    article = Article.objects.get(title='タイトル')
    self.assertEqual('投稿内容', article.post)
  

class ArticleDetailTest(TestCase):
  def setUp(self):
    self.user = UserModel.objects.create(
      username="test_user",
      email="test@example.com",
      password="secret1",
    )
    self.article = Article.objects.create(
      title="タイトル",
      post="牛島の塩",
      created_by=self.user,
    )
  
  def test_should_use_expected_template(self):
    response = self.client.get("/articles/%s/" % self.article.id)
    self.assertTemplateUsed(response, "articles/article_detail.html")
  
  def test_top_page_returns_200_and_expected_heading(self):
    response = self.client.get("/articles/%s/" % self.article.id)
    self.assertContains(response, self.article.title, status_code=200)

class EditArticleTest(TestCase):
  def test_should_resolve_article_edit(self):
    found = resolve("/articles/1/edit/")
    self.assertEqual(article_edit, found.func)