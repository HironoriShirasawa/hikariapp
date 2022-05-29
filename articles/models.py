from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

from sorl.thumbnail import get_thumbnail, delete

import uuid

def image_directory_path(instance, filename):
  return 'images/{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

class Article(models.Model):
  title = models.CharField('タイトル', max_length=128)
  class Region(models.TextChoices):
    Ushima = '牛島','牛島'
    IhokiGokenya = '伊保木・五軒家','伊保木・五軒家'
    Murodumi = '室積','室積'
    Mitsui = '光井','光井'
    Shimata = '島田','島田'
    Asae = '浅江','浅江'
    Mii = '三井','三井'
    Suoh = '周防','周防'
    Yamato = '大和','大和'
    City = '光市','全域'
    Etc = 'その他地域','その他'
  
  region = models.TextField(choices=Region.choices, verbose_name='地域')

  class Classification(models.TextChoices):
    politics = '政治','政治'
    administration = '行政','行政'
    bussiness = '企業','企業'
    culture = '文化','文化'
    sports = 'スポーツ','スポーツ'
    nature = '自然','自然'
    school = '学校','学校'
    person = '人物','人物'
    etc = 'その他','その他'
  
  classification = models.TextField(choices=Classification.choices, verbose_name='分類')
  post = models.TextField('投稿内容')
  article_image = models.ImageField(null=True, blank=True, verbose_name="画像", upload_to=image_directory_path)
  def save(self, *args, **kwargs):
    super(Article, self).save(*args, **kwargs)
    temp_img_name = self.article_image.name
    if self.article_image.width > 500 or self.article_image.height > 500:
      new_width = 500
      new_height = 500

      resized = get_thumbnail(self.article_image, "{}x{}".format(new_width, new_height))
      name = resized.name.split('/')[-1]
      self.article_image.save(name, ContentFile(resized.read()), True)
      try:
        delete(temp_img_name)
      except "NotFound":
        pass
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name="投稿者",
                                on_delete=models.CASCADE)
  created_at = models.DateTimeField("投稿日", auto_now_add=True)

  def __str__(self):
    return self.title

class Comment(models.Model):
  text = models.TextField("本文", blank=False)
  commented_at = models.DateTimeField("投稿日", auto_now_add=True)
  commented_to = models.ForeignKey(Article, 
                                  verbose_name="記事", 
                                  on_delete=models.CASCADE)
  commented_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  verbose_name="投稿者",
                                  on_delete=models.CASCADE)
  def __str__(self):
    return self.text