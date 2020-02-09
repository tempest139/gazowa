#!/usr/bin/env python2
#coding:utf-8
# pip install Pillow

# アップデート日 : 2019/11/24
# Interfaceから削除をPictureに移してメソッド化
# コンストラクタで画像をロードする
# つまりPictureクラスのインスタンス作成=画像のインスタンスにする

import WxInterface
import gtk
import subprocess

# 3つ以上の起動を防止する
cmd = "ps ax | grep 'python /home/martin/python/gazowa/marpic_v2.py'"
script_name = 'python /home/martin/python/gazowa/marpic_v2.py'
ret = subprocess.check_output( cmd , shell=True)
number = ret.count( script_name ) - 2
if( number >= 3 ):
    sys.exit()

WxInterface.WxInterface()
gtk.main()
