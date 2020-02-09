#!/usr/bin/env python
#coding:utf-8
#LAST_UPDATE:2015/3/23
import gtk
import subprocess
import sys
import os
import Image
import shutil

class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp,self).__init__()

        #コマンドライン引数からファイル名とディレクトリパスを取得
        self.args = sys.argv
        if(len(self.args)>1):
            path = self.args[1]
            num = path.rfind("/")
            self.filename = path[num+1:]
            self.filepath = path[:num+1]

        # 全画面表示のフラグ
        self.screenFlag = True
        # 画像の回転方向のフラグ
        self.mouseRotateFlag = False
        self.fixFlag = True
        # シフトを押しているかどうかのフラグ
        self.shift_Flag = False
        self.rotate = 0
        # 画像の水平反転のフラグ
        self.flip_LR = False
        # 画像の上下反転フラグ
        self.flip_TB = False
        # 画像の背景カラーフラグ
        self.back_color = False
        
        #---------------WINDOW---------------------
        #バックカラー
        self.color = gtk.gdk.color_parse('#000000')
        self.modify_bg(gtk.STATE_NORMAL, self.color)

        self.set_title(self.filename)
        self.connect("destroy",gtk.main_quit)
        self.connect("realize",self.hide_mouse)
        #ウインドウイベント
        self.connect("window_state_event",self.window_change)

        #イベント処理
        self.add_events(gtk.gdk.KEY_PRESS_MASK|gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.SCROLL_MASK|gtk.gdk.WINDOW_STATE_ICONIFIED)
        self.connect("key-press-event",self.key_event)
        self.connect("key-release-event",self.key_release_event)
        self.connect("button-press-event", self.mouse_button_event)
        self.connect("scroll-event",self.mouse_scroll_event)

        self.set_size_request(250,150)
        self.set_position(gtk.WIN_POS_CENTER)
        
        #filelist:ディレクトリ内の画像ファイルの一覧
        self.filelist = self.get_dirimage( self.filepath )
        self.filelist.sort()
        #self.number:現在の画像ファイルの番号
        self.number = self.filelist.index(self.filename)
        for i in self.filelist:
            print i

        self.fix = gtk.Fixed()
        tmp = self.load_image( self.filepath + self.filename )
        self.set_image(tmp)
        self.show_all()
        
        self.fullscreen()

        self.mouseRotateFlag = True
        self.rotate_update(1)

    #マウス非表示
    def hide_mouse(self,widget):
        pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
        color = gtk.gdk.Color()
        cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
        widget.window.set_cursor(cursor)
    
    def window_change(self,widget,event):
        pass
        #print event.new_window_state

    #ショートカットキー入力で呼ばれる関数
    def key_event(self,widget,event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        #print event.type
        print keyname
        if(keyname=="F11" or keyname=="f"):
            #全画面表示の切り替え
            if(self.screenFlag == True):
                self.screenFlag = not(self.screenFlag)
                self.unfullscreen()
                self.maximize()
            elif(self.screenFlag == False):
                self.screenFlag = not(self.screenFlag)
                self.fullscreen()
        if(keyname=="Home"):
            self.update("home")
        if(keyname=="End"):
            pass
        if(keyname=="Delete"):
            #もしShiftキーを押していれば
            if( self.shift_Flag == True ):
                #ファイルを削除する
                hoge = self.filepath + self.filelist[self.number]
                os.remove(hoge)
                print "削除:",hoge
                #更新
                self.sc_update()
        if(keyname=="D"):
            #ファイルを削除する
            hoge = self.filepath + self.filelist[self.number]
            os.remove(hoge)
            print "削除:",hoge
            #更新
            self.sc_update()
        if(keyname=="q"):
            sys.exit()
        #画像を一時的に移動する
        if(keyname=="M"):
            target = self.filepath + self.filelist[self.number]
            shutil.move( target , os.environ["HOME"] )
            self.sc_update()
        if(keyname=="c"):
            # もしバックカラーが白なら
            if(self.back_color == True):
                # 黒にする
                self.color = gtk.gdk.color_parse('#000000')
                self.modify_bg(gtk.STATE_NORMAL, self.color)
                self.back_color = False
            else:
                self.color = gtk.gdk.color_parse('#FFFFFF')
                self.modify_bg(gtk.STATE_NORMAL, self.color)
                self.back_color = True
        if(keyname=="h"):
            #画像を水平に反転する
            self.flip_LR = not(self.flip_LR)
            self.image_ch()
        if(keyname=="H"):
        #左右反転して保存
            try:
                im = Image.open( self.filepath + self.filelist[self.number] )
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
                im.save( self.filepath + self.filelist[self.number], quality = 100 )
                print "画像反転完了",self.filepath + self.filelist[self.number]
                self.image_ch()
            except:
                print "画像反転失敗"
        if(keyname=="u"):
            #画像を垂直に反転する
            self.flip_TB = not(self.flip_TB)
            self.image_ch()
        if(keyname=="U"):
        #上下反転して保存
            try:
                im = Image.open( self.filepath + self.filelist[self.number] )
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
                im.save( self.filepath + self.filelist[self.number], quality = 100 )
                print "画像反転完了",self.filepath + self.filelist[self.number]
                self.image_ch()
            except:
                print "画像反転失敗"
        if(keyname=="Up"):
            self.update("up")
        if(keyname=="Down"):
            self.update("down")
        if(keyname=="space"):
            self.update("up")
        if(keyname=="Left" or keyname=="l"):
            self.mouseRotateFlag = False
            self.rotate_update(2)
        if(keyname=="Right" or keyname=="r"):
            self.mouseRotateFlag = True
            self.rotate_update(1)
        if(keyname=="Escape"):
            self.flip_LR = False
            self.flip_TB = False
            self.mouseRotateFlag = False
            self.rotate_update(0)
        if(keyname=="Shift_L" or keyname=="Shift_R"):
            self.shift_Flag = True
            print "Shift",self.shift_Flag


    #キーボードを離した時の処理
    def key_release_event(self,widget,event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        #print keyname
        if(keyname == "Shift_L" or keyname == "Shift_R"):
            self.shift_Flag = False
            print "Shift",self.shift_Flag

    #マウス入力
    def mouse_scroll_event(self,widget,event):
        if(event.direction == gtk.gdk.SCROLL_UP):
            self.update("up")
        if(event.direction == gtk.gdk.SCROLL_DOWN):
            self.update("down")

    #マウスボタン入力
    def mouse_button_event(self,widget,event):
        #print event.button
        #左クリックかつダブルクリックじゃない場合
        if(event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS):
            self.update("down")
        #右クリックかつダブルクリックで終了
        if(event.button == 3 and event.type == gtk.gdk._2BUTTON_PRESS):
            sys.exit(0)
        #中クリックでフルスクリーン
        if(event.button == 2 and event.type == gtk.gdk.BUTTON_PRESS):
            #全画面表示の切り替え
            if(self.screenFlag == True):
                self.screenFlag = not(self.screenFlag)
                self.unfullscreen()
                self.maximize()
            elif(self.screenFlag == False):
                self.screenFlag = not(self.screenFlag)
                self.fullscreen()
        #上サイドクリック(回転)
        if(event.button == 9 and event.type == gtk.gdk.BUTTON_PRESS):
            if(self.mouseRotateFlag == False):
                self.mouseRotateFlag = not(self.mouseRotateFlag)
                self.rotate_update(1)
            elif(self.mouseRotateFlag == True):
                self.mouseRotateFlag = not(self.mouseRotateFlag)
                self.rotate_update(2)
        #下サイドクリック
        if(event.button == 8):            
            if(self.fixFlag == True and event.type == gtk.gdk.BUTTON_PRESS):
                self.fix.hide()
                self.fixFlag = not(self.fixFlag)
            elif(self.fixFlag == False and event.type == gtk.gdk.BUTTON_PRESS):
                self.fix.show()
                self.fixFlag = not(self.fixFlag)

    #ロードした画像オブジェクトtmpを加工して画面に表示する
    def set_image(self,tmp):
        #画像変数
        width = tmp.get_width()
        height = tmp.get_height()
        screenx = gtk.gdk.screen_width()
        screeny = gtk.gdk.screen_height()

        image = gtk.Image()
        new_width = int(height*float(screeny)/width)
        if(self.rotate>0 and height>=width):
            if(new_width<=screenx):
                tmp = self.set_rotation(self.rotate,tmp)
                tmp = tmp.scale_simple(new_width,screeny,gtk.gdk.INTERP_HYPER)
                image.set_from_pixbuf(tmp)
                self.fix.put(image,(screenx-new_width)/2,0)
            elif(new_width>screenx):
                new_height = int(width*float(screenx)/height)
                tmp = self.set_rotation(self.rotate,tmp)
                tmp = tmp.scale_simple(screenx,new_height,gtk.gdk.INTERP_HYPER)
                image.set_from_pixbuf(tmp)
                self.fix.put(image,0,(screeny-new_height)/2)
        elif(self.rotate==0 or height<width):
            new_width = int(width*float(screeny)/height)
            if(new_width<=screenx):
                tmp = self.set_flip(self.flip_LR , self.flip_TB , tmp)
                tmp = tmp.scale_simple(new_width,screeny,gtk.gdk.INTERP_HYPER)
                image.set_from_pixbuf(tmp)
                self.fix.put(image,(screenx-new_width)/2,0)
            else:
                tmp = self.set_flip(self.flip_LR,self.flip_TB,tmp)
                new_height = int(height*float(screenx)/width)
                tmp = tmp.scale_simple(screenx,new_height,gtk.gdk.INTERP_HYPER)
                image.set_from_pixbuf(tmp)
                self.fix.put(image,0,(screeny-new_height)/2)
        self.add(self.fix)

    #アイコン設定
    def set_icon(self,path):
        try:
            self.set_icon_from_file(path)
        except Exception,e:
            print e.message
            sys.exit(1)

    #画像を回転させる
    def set_rotation(self,rotate,tmp):
        if(rotate==0):
            pass
        if(rotate==1):
            tmp = tmp.rotate_simple(270)
        if(rotate==2):
            tmp = tmp.rotate_simple(90)
        return tmp
    
    #画像を左右上下反転させる
    def set_flip(self , flip_LR , flip_TB , tmp):
        if(flip_LR==True):
            tmp = tmp.flip(True)
        if(flip_TB==True):
            tmp = tmp.flip(False)
        return tmp

    #画像ファイルをロードする
    def load_image(self,path):
        try:
            tmp = gtk.gdk.pixbuf_new_from_file(path)
        except Exception,e:
            #もしロードできなければ,ディレクトリ内の画像リストをもう一度更新する
            self.filelist = self.get_dirimage(self.filepath)
            self.filelist.sort()
            #画像を消したので画像のリストの番号を一つ後ろにする
            if(self.number>=(len(self.filelist)-1)):
                self.number = 0
            else:
                self.number += 1

            #もう一度再帰呼出し
            #self.load_image(path)

        return tmp

    #ディレクトリ内の画像をリストに取得    
    def get_dirimage(self,path):
        files = os.listdir(path)
        list = []
        for i in files:
            if((".jpg"in i) == True or (".jpeg"in i) == True or (".png"in i) == True or (".JPG"in i) == True or (".bmp"in i) == True or (".gif"in i) == True):
                list.append(i)

        return list

    #回転命令時に呼ばれる関数
    def rotate_update(self,a):
        self.rotate = a
        self.image_ch()
        
    #表示画面を次の画像に変える関数
    def update(self,a):
        if(a=="up"):
            if(self.number == 0):
                self.number = len(self.filelist)-1
            else:
                self.number -= 1
            self.image_ch()

        elif(a=="down"):
            if(self.number>=(len(self.filelist)-1)):
                self.number = 0
            else:
                self.number += 1
            self.image_ch()
                        
        elif(a=="home"):
            self.number = 0
            self.image_ch()            
        else:
            print "self.update()：エラー"

        self.set_title(self.filelist[self.number])

    # self.update()などから呼ばれる画像表示を変更する関数
    def image_ch(self):
        # もしディレクトリ内に画像がなければ終了する
        if( len(self.filelist) == 0 ):
            sys.exit()
        self.remove(self.fix)
        self.fix = None
        self.fix = gtk.Fixed()
        try:
            tmp = self.load_image( self.filepath + self.filelist[self.number] )
            self.set_image(tmp)
        except:
            pass
        self.show_all()

    # 画面行進
    def sc_update(self):
        #ディレクトリリスト更新
        self.filelist = self.get_dirimage(self.filepath)
        self.filelist.sort()
        #画像を消したので画像のリストの番号を一つ後ろにする
        if(self.number == 0):
            self.number = len(self.filelist) - 1
        else:
            self.number -= 1
        #そして次の画像表示
        self.update("down")


#多重起動防止関数
def prevent_multi_process():
    cmd = "ps ax | grep 'python /home/martin/python/gazowa_flip.py'"
    ret = subprocess.check_output( cmd , shell=True)
    #print ret
    script_name = 'python /home/martin/python/gazowa_flip.py'
    number = ret.count(script_name)
    #上のpsコマンドとgrepの数を減らす
    number -= 2
    print "がぞわーの起動数:",number,"個"
    if( number >= 3 ):
        print "多重起動禁止(3つ以上の起動は禁止しています)"
        sys.exit()

prevent_multi_process()
PyApp()
gtk.main()
