#articles内で使用する独自メソッドをまとめる

import requests
from datetime import datetime
from PIL import Image

#縦横比を保ったまま画像サイズを調整する関数
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

#今日、明日の天気予報を返す関数
def weather(city_code, url):
  response = requests.get(url)
  weather_json = response.json()
  now_hour = datetime.now().hour 
  cor = weather_json['forecasts'][0]['telop']
  cor_tomorrow = weather_json['forecasts'][1]['telop']
  return cor, cor_tomorrow