from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from .models import Article, Comment 
from .forms import ArticleForm, CommentForm

from PIL import Image

#縦横比を保ったまま画像サイズを調整する関数を定義
def keepAspectResize(path, size):
  image = Image.open(path)
  width, height = size
  x_ratio = width / image.width
  y_ratio = height / image.height
  #画像の幅と高さ両方に小さい方の比率を掛けてリサイズ後のサイズを計算
  if x_ratio < y_ratio:
    resize_size = (width, round(image.height * x_ratio))
  else:
    resize_size = (round(image.width * y_ratio), height)
  #リサイズ後の画像サイズにリサイズする
  resize_image = image.resize(resize_size)

  return resized_image

def top(request):
  articles = Article.objects.all()
  context = {"articles": articles}
  return render(request, "articles/top.html", context)

@login_required
def article_new(request):
  if request.method == "POST":
    form = ArticleForm(request.POST, request.FILES)
    if form.is_valid():
      article = form.save(commit=False)
      article.created_by = request.user
      article.save()
      return redirect(article_detail, article_id=article.pk)
  else:
    form = ArticleForm()
  return render(request, "articles/article_new.html", {'form': form})

@login_required
def article_edit(request, article_id):
  article = get_object_or_404(Article, pk=article_id)
  if article.created_by_id != request.user.id:
    return HttpResponseForbidden("この記事の編集は許可されていません。")
  
  if request.method == "POST":
    form = ArticleForm(request.POST, request.FILES, instance=article)
    if form.is_valid():
      form.save()
      return redirect('article_detail', article_id=article_id)
  else:
    form = ArticleForm(instance=article)
  return render(request, 'articles/article_edit.html', {'form': form})
  
@login_required
def article_detail(request, article_id):
  article = get_object_or_404(Article, pk=article_id)
  comments = Comment.objects.filter(commented_to=article_id).all()
  comment_form = CommentForm()

  return render(request, "articles/article_detail.html", {
    'article': article,
    'comments': comments,
    'comment_form': comment_form,
  })

@login_required
def comment_new(request, article_id):
  article = get_object_or_404(Article, pk=article_id)

  form = CommentForm(request.POST)
  if form.is_valid():
    comment = form.save(commit=False)
    comment.commented_to = article
    comment.commented_by = request.user 
    comment.save()
    messages.add_message(request, messages.SUCCESS,
                        "コメントを投稿しました。")
  else:
    messages.add_message(request, messages.ERROR,
                        "コメントの投稿に失敗しました。")
  return redirect('article_detail', article_id=article_id)