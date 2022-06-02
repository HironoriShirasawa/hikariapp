ある地域に住む方、ある地域に興味のある方が交流することを目的としたDjangoで制作したWebアプリです。

投稿には画像を貼り付けられるようにしています。
また、会員登録機能やパスワード変更機能も付けています。

プロジェクトをpullした際には、settings_local_sample.pyをコピーしてsettings_local.pyファイルを作成し、値を定義して使用してみてください。
SECRET_KEYの再生成の方法
プロジェクト直下にて
$ python manage.py shell
対話モードにて
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secretkey()
出力された文字列を、SECRET_KEYに設定してください。


![2022-05-30 (1)](https://user-images.githubusercontent.com/80143448/170892967-f0fa0eb3-33bb-4601-bfe6-19ce82357bd4.png)


