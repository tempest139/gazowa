#!/usr/bin/env python2
#coding:utf-8

# GUIのためのクラス
# https://developer.gnome.org/pygtk/stable/class-gtkfixed.html
import gtk
# 左右、上下反転のためのクラス
from PIL import Image

import subprocess
import sys
import os
import shutil
import requests
import hashlib

class WxPicture():
    #重要: コンストラクタでgtk.Windowクラスのインスタンスを受け取るよ!
    def __init__( self , preWindow ):
        self.window = preWindow
        self.window.fix = gtk.Fixed()
        # 画像の回転フラグ
        self.rotate = False
        # 画像の回転方向のフラグ False:右 True:左
        self.rotateDir = True
        # 画像の水平反転のフラグ
        self.flip_LR = False
        # 画像の上下反転フラグ
        self.flip_TB = False

        #コマンドライン引数からファイル名とディレクトリパスを取得
        self.args = sys.argv
        if( len( self.args ) > 1 ):
            path = self.args[1]
            num = path.rfind("/")
            self.filename = path[num+1:]
            self.filepath = path[:num+1]

        # filelist : ディレクトリ内の画像ファイルの一覧
        self.filelist = self.getList( self.filepath )
        self.filelist.sort()
        # self.number : 現在の画像ファイルの番号
        self.number = self.filelist.index( self.filename )
        for i in self.filelist:
            print i
        self.setImage()

    # 画像オブジェクトself.tmpを回転リサイズして画面に表示する
    def setImage( self ):        
        self.tmp = gtk.gdk.pixbuf_new_from_file( self.path() )
        self.width = self.tmp.get_width()
        self.height = self.tmp.get_height()
        screenX = gtk.gdk.screen_width()
        screenY = gtk.gdk.screen_height()
        image = gtk.Image()
        # 回転する & 縦>横なら
        if self.rotate == True and self.height >= self.width:
            if self.rotateDir == True:
                self.tmp = self.tmp.rotate_simple(90)
            elif self.rotateDir == False:
                self.tmp = self.tmp.rotate_simple(270)
            if (self.width * screenX / self.height) < screenY:
                new_width = screenX
                new_height = int( self.width * float( screenX ) / self.height )
                self.tmp = self.tmp.scale_simple( new_width , new_height , gtk.gdk.INTERP_HYPER )
                image.set_from_pixbuf( self.tmp )
                self.window.fix.put( image , 0 , ( screenY - new_height ) / 2 )
            else:
                new_width = int( self.height * float( screenY ) / self.width )
                new_height = screenY
                self.tmp = self.tmp.scale_simple( new_width , new_height , gtk.gdk.INTERP_HYPER )
                image.set_from_pixbuf( self.tmp )
                self.window.fix.put( image , ( screenX - new_width ) / 2 , 0 )
        # 回転しない & 横>縦なら
        else:
            hoge = int( screenY * float( self.width ) / self.height )
            if screenX >= hoge or self.height >= self.width:
                new_height = screenY
                new_width = hoge
                self.tmp = self.tmp.scale_simple( new_width , new_height , gtk.gdk.INTERP_HYPER )
                image.set_from_pixbuf( self.tmp )
                self.window.fix.put( image , ( screenX - new_width ) / 2 , 0 )
            else:
                new_width = screenX
                new_height = int( screenX * float( self.height ) / self.width )
                self.tmp = self.tmp.scale_simple( new_width , new_height , gtk.gdk.INTERP_HYPER )
                image.set_from_pixbuf( self.tmp )
                self.window.fix.put( image , 0 , ( screenY - new_height ) / 2 )
        self.window.add( self.window.fix )
        self.window.show_all()
        self.window.set_title( self.path() )
    # 画像を削除する
    def delImage( self ):
        os.remove( self.path() )
        self.number -= 1
        self.filelist = self.getList( self.filepath )
        self.filelist.sort()
        self.next()

    #画像をめくる
    def next( self ):
        self.deleteScreen()
        self.listNext()
        if self.rotate == True and ( self.height > self.width ):
            if self.rotateDir == True:
                self.rotateL()
            else:
                self.rotateR()
        else:
            self.setImage()
        
    def prev( self ):
        self.deleteScreen()
        self.listPrev()
        if self.rotate == True and ( self.height > self.width ):
            if self.rotateDir == True:
                self.rotateL()
            else:
                self.rotateR()
        else:
            self.setImage()

    #画像を回転させる
    def rotateR( self ):
        self.rotate = True
        self.rotateDir = False
        if self.height > self.width:
            self.deleteScreen()
            self.setImage()
    def rotateL( self ):
        self.rotate = True
        self.rotateDir = True
        if self.height > self.width:
            self.deleteScreen()
            self.setImage()

    """
    #画像を左右上下反転させる
    def set_flip( self ):
        if self.flip_LR == True :
            self.tmp = self.tmp.flip(True)
        if self.flip_TB == True :
            self.tmp = self.tmp.flip(False)
        return self.tmp
    """

    # pathの画像リストを取得する
    def getList( self , path ):
        files = os.listdir( path )
        list = []
        for i in files:
            if((".jpg"in i) == True or (".jpeg"in i) == True or (".png"in i) == True or (".JPG"in i) == True or (".bmp"in i) == True or (".gif"in i) == True):
                list.append(i)
        if len( list ) <= 1:
            self.number = 0
        return list

    # filelist配列を計算する
    def listPrev( self ):
        if self.number == 0:
            self.number = len( self.filelist ) - 1
        else:
            self.number -= 1
    def listNext( self ):
        if self.number == len( self.filelist ) - 1  :
            self.number = 0
        else:
            self.number += 1
    # 描画スクリーンを初期化する
    def deleteScreen(self):
        self.window.remove( self.window.fix )
        self.window.fix = None
        self.window.fix = gtk.Fixed()
    # 現在のパスを取得
    def path(self):
        return self.filepath + self.filelist[self.number]
    # 画像を詳細検索する
    def search( self ):
        url = "https://ascii2d.net/search/file/"
        name = self.path()
        file = { 'upload_file': open( name , 'rb' ) }
        res = requests.post( url , files=file)
        print(res.status_code)
        with open( path , "rb" ) as tmp:
            data = tmp.read()
        value = hashlib.md5(data).hexdigest()
        url = "https://ascii2d.net/search/color/" + value
        subprocess.call( "chromium-browser " + url , shell=True )
