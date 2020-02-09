#!/usr/bin/env python2
#coding:utf-8

# GUIのためのクラス
import gtk
# 左右、上下反転のためのクラス
from PIL import Image


import WxPicture
import subprocess
import sys
import os
import shutil

class WxInterface():
    def __init__( self ):
        # 全画面表示のフラグ
        self.screenFlag = True
        # 画面表示フラグ
        self.fixFlag = True

        # gtkクラスインスタンス作成
        self.window = gtk.Window()
        # Pictureクラスインスタンスの作成
        self.picture = WxPicture.WxPicture( self.window )

        #バックカラー
        self.window.color = gtk.gdk.color_parse('#000000')
        self.window.modify_bg(gtk.STATE_NORMAL, self.window.color)
        self.window.connect( "destroy" , gtk.main_quit )
        #self.window.connect( "realize" , self.hide_mouse )
        #イベント処理
        self.window.connect("window_state_event",self.window_change)
        self.window.add_events(gtk.gdk.KEY_PRESS_MASK|gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.SCROLL_MASK|gtk.gdk.WINDOW_STATE_ICONIFIED)
        self.window.connect( "key-press-event" , self.key_event )
        self.window.connect( "button-press-event" , self.mouse_button_event )
        self.window.connect( "scroll-event" , self.mouse_scroll_event )
        #タイトルとサイズとか
        self.window.set_title( self.picture.filename )
        self.window.set_size_request( 250 , 150 )
        self.window.set_position( gtk.WIN_POS_CENTER )

        self.picture.setImage()
        self.window.show_all()
        self.window.fullscreen()

    #マウス非表示
    def hide_mouse(self,widget):
        pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
        color = gtk.gdk.Color()
        cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
        widget.window.set_cursor(cursor)
    
    def window_change(self,widget,event):
        pass

    #ショートカットキー関数
    def key_event(self,widget,event):
        keyname = gtk.gdk.keyval_name( event.keyval )
        print( keyname , type(keyname) )
        if keyname == "f":
            self.fullscreen()
        if keyname == "D":
            self.picture.delImage()
        if keyname == "q":
            sys.exit()
        if keyname == "h":
            self.flip_LR = not( self.picture.flip_LR )
            self.picture.setImage()
        if keyname == "u":
            self.flip_TB = not(self.pictureflip_TB)
            self.picture.setImage()
        # 画像詳細検索
        if keyname == "S":
            self.picture.search()
        #左右反転して画像保存
        if keyname == "H":
            try:
                im = Image.open( self.picture.filepath + self.picture.filelist[self.picture.number] )
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
                im.save( self.picture.filepath + self.picture.filelist[self.picture.number], quality = 100 )
                self.picture.setImage()
            except:
                pass
        #上下反転して画像保存
        if keyname == "U":
            try:
                im = Image.open( self.picture.filepath + self.picture.filelist[self.picture.number] )
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
                im.save( self.picture.filepath + self.picture.filelist[self.picture.number], quality = 100 )
                self.picture.setImage()
            except:
                pass
        if keyname == "Up":
            self.picture.prev()
        if keyname == "Down":
            self.picture.next()
        if keyname == "space":
            self.picture.prev()
        if keyname == "Left" or keyname == "l":
            self.picture.rotateL()
        if keyname == "Right" or keyname == "r":
            self.picture.rotateR()
        if keyname == "Escape":
            self.picture.rotate = False
            self.picture.flip_LR = False
            self.picture.flip_TB = False
            self.picture.listPrev()
            self.picture.next()

    #マウススクロール関数
    def mouse_scroll_event(self,widget,event):
        if(event.direction == gtk.gdk.SCROLL_UP):
            self.picture.prev()
        if(event.direction == gtk.gdk.SCROLL_DOWN):
            self.picture.next()

    #マウスボタン関数
    def mouse_button_event(self,widget,event):
        #左クリック
        if(event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS):
            self.picture.next()
        #右ダブルクリック(終了)
        if(event.button == 3 and event.type == gtk.gdk._2BUTTON_PRESS):
            sys.exit(0)
        #中クリック(フルスクリーン)
        if(event.button == 2 and event.type == gtk.gdk.BUTTON_PRESS):
            self.fullscreen()
        #上サイドクリック(回転)
        if(event.button == 9 and event.type == gtk.gdk.BUTTON_PRESS):
            if self.picture.rotateDir == False:
                self.picture.rotateL()
            elif self.picture.rotateDir == True:
                self.picture.rotateR()
        #下サイドクリック
        if(event.button == 8):            
            if(self.fixFlag == True and event.type == gtk.gdk.BUTTON_PRESS):
                self.window.fix.hide()
                self.fixFlag = not( self.fixFlag )
            elif(self.fixFlag == False and event.type == gtk.gdk.BUTTON_PRESS):
                self.window.fix.show()
                self.fixFlag = not( self.fixFlag )

    #フルスクリーン
    def fullscreen( self ):
        if self.screenFlag == True:
            self.screenFlag = not( self.screenFlag )
            self.window.unfullscreen()
            self.window.maximize()
        elif self.screenFlag == False:
            self.screenFlag = not( self.screenFlag )
            self.window.fullscreen()

    #アイコン設定
    def set_icon( self , path ):
        try:
            self.set_icon_from_file( path )
        except(Exception,e):
            print( e.message )
            sys.exit(1)
