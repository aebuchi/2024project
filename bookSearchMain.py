# Tkinterをインポート
import tkinter as tk
import json
import jsonDecode
import acquisitionImage
from tkinter import ttk
from PIL import ImageTk, Image

# Tkオブジェクトを生成
root = tk.Tk()
# ウィンドウのタイトルを設定
root.title('書籍検索')
# ウィンドウの内部サイズを設定
root.geometry('900x480')

# 検索ワード入力テキストエリア指定
tex = tk.Text( background = '#FFFFFF')
tex.place( x = 20, y = 10, width = 200, height = 25 )

# 一覧の奇数行に背景色を付けるための関数定義
def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
        elm[:2] != ('!disabled', '!selected')]

# 検索結果一覧の全てのiidを取得
def get_iids(item=None):
    for child in tree.get_children(item):
        yield child
        yield from get_iids(child)

# 検索ボタンクリック時に呼び出す関数を定義
def search_botton():
    # まだ何もしない
    #pass
    # 表示済み一覧の削除
    iids = list(get_iids())
    print(iids)
    for i in iids:
        tree.delete(i)
    
    # テキストエリアの入力値を取得
    s = tex.get(0., tk.END)
    message = tk.Message(text=s)
    # ここがあるとテキストエリアの入力値が画面上に表示される
    # message.pack()
    print(s)

    # 書籍検索API検索結果取得(テスト中)
    jd = jsonDecode.JsonDecode()
    bookList = jd.json_decode(s)
    no = 1
    for i in bookList:
        #print(i)
        book = json.loads(i)
        # 書籍説明文が長すぎて枠内に収まらないので改良が必要(Json取得時に枠内に収まるよう、文字長を調整する必要あり)
        # 上記とは別に説明文の全量を隠し項目として保持必要あり(詳細画面の表示に必要)
        tree.insert(parent='', index=no, tags=no, values=(
            book['no'], book['title'], book['authors'], book['bookDescriptionExistence'], book['pageCount'],
            book['thumbnailExistence'], book['thumbnailUrl'], book['bookDescription']))

        if no % 2 == 0:
            # tagが奇数(レコードは偶数)の場合のみ、背景色の設定
            tree.tag_configure(book['no'],background="#CCFFFF")

        # indexとtagsの番号をカウントアップ
        no+=1

# 選択行選択時のイベント
def check_record(event):
    # 選択行のレコード取得
    record_id = tree.focus()
    print("選択行ID：" + record_id)
    # 選択行のレコードを取得
    record_values = tree.item(record_id, 'values')
    print(record_values[1])
    # 詳細ウィンドウサイズ定義(実際のウィンドウとサムネ用キャンバスのサイズで使用するため)
    windowSizeWidth = '900'
    windowSizeHeight = '600'
    # 詳細ウィンドウ表示
    detail = tk.Toplevel()
    # 詳細ウィンドウの内部サイズを設定
    detail.geometry(windowSizeWidth + 'x' + windowSizeHeight)
    # 詳細ウィンドウのタイトルを設定
    detail.title('詳細画面')
    # 詳細内容設定

    # サムネイル画像の表示位置を先に決める関係で、書籍説明文を指定文字数で区切った時の要素数を算出
    # 書籍説明文全文を75文字毎に区切り配列に格納
    descriptionTextList = [record_values[7][x:x+75] for x in range(0, len(record_values[7]), 75)]
    count = len(descriptionTextList)

    # 先にサムネ用のキャンバス指定と読み込みサムネ画像の読み込みを行う(その後でキャンバス上に文字情報を上書き)
    
    # サムネ画像を取得
    ai = acquisitionImage.WebImage()
    picturePass = ai.acquisitionThumbnail(record_values[6])
    # 画像読み込み
    img = Image.open(picturePass)# 画像の読み込み

    # Pillowで読み込んだ画像をtkinterで表示できるよう設定
    tk_image = ImageTk.PhotoImage(image=img)
    # 画面サイズと同じキャンバスを作成する（キャンバス自体の表示位置が変更できなかったため）
    cvs = tk.Canvas(master=detail, width=windowSizeWidth, height=windowSizeHeight)
    #cvs.propagate(False)
    # キャンバス内の画像表示位置指定とその他の定義(高さの位置は書籍説明分の区切り数に応じて変更)
    cvs.create_image(100, 110 + (15 * count), anchor='nw', image=tk_image)
    cvs.pack()

    label_title = tk.Label(detail, text='タイトル：' + record_values[1])
    label_title.place(x = '10', y = '10')
    label_authors = tk.Label(detail, text='著者：' + record_values[2])
    label_authors.place(x = '10', y = '35')
    # 書籍説明文が長すぎてウィンドウ内に収まらないので改良が必要
    # 適度なところで改行した場合、ページ数・サムネの表示位置の調整も必要
    descriptionText = ""
    print("カウント：" + str(len(descriptionTextList)))
    for text in descriptionTextList:
        descriptionText += text + '\n'
    label_description = tk.Label(detail, text='書籍説明：' + descriptionText, anchor=tk.W, justify='left')
    label_description.place(x = '10', y = '60')
    # ページ数の基本表示位置(縦位置)
    pageCountHeightPoint = 85 + (15 * count)
    label_pageCount = tk.Label(detail, text='ページ数：' + record_values[4])
    label_pageCount.place(x = '10', y = str(pageCountHeightPoint))
    # サムネイルの基本表示位置(縦位置)
    pageCountHeightPoint = 110 + (15 * count)
    label_imageLinks = tk.Label(detail, text='サムネイル：')
    label_imageLinks.place(x = '10', y = str(pageCountHeightPoint))
    # サムネ画像の取得
    #ai = acquisitionImage.WebImage()
    #thumbnail = ai.acquisitionThumbnail(record_values[5])
    #ai.acquisitionThumbnail(record_values[5])
    # imageの読み込み
    # load = tk.PhotoImage()
    #label_imageLinks = tk.Label(detail, image = ImageTk.PhotoImage(thumbnail))
    #label_imageLinks.place(x = '10', y = '110')
    # ローカルに保存したサムネ画像を取得
    #img = Image.open('./temp/thumbnail.jpg')
    #imageLabel = tk.Label(detail, image=img)
    #imageLabel.Image = thumbnail
    #imageLabel.pack()

    detail.mainloop()

# ボタンの作成はButtonを使用する。commandにて実行関数を指定する。
button = tk.Button(root, text="検索", command=search_botton)
# placeプロパティにて配置箇所をX,Y座標で指定する
button.place(x=230, y=10, width = 50, height = 25)

# 一覧の背景色を設定する定義
style = ttk.Style()  
style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
tree = ttk.Treeview(
    root,
    show = "headings",
    )

# Treeviewの生成
tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7, 8), show='headings', height=20)
tree.bind("<<TreeviewSelect>>", check_record)
# 各列の設定
tree.column(1,width=25)  # No
tree.column(2,width=200) # タイトル
tree.column(3,width=150) # 著者
tree.column(4,width=350) # 説明文
tree.column(5,width=60)  # ページ数
tree.column(6,width=100) # サムネ
tree.column(7,width=100) # サムネ用URL(非表示項目)
tree.column(8,width=100) # 説明文全量(非表示項目)
# 列の見出し設定
tree.heading(1, text="No")
tree.heading(2, text="タイトル")
tree.heading(3, text="著者")
tree.heading(4, text="書籍についての説明文")
tree.heading(5, text="ページ数")
tree.heading(6, text="表紙")
tree.heading(7, text="サムネURL")
tree.heading(8, text="説明文全量")

tree["displaycolumns"]=("1","2","3","4","5","6")

# レコードの初期表示(ハードコーディングのため、本来不要)
'''
tree.insert(parent='', index=0, tags=0, values=(1, "タイトル１", "書いた人１", "説明１", "ページ数１", "サムネ１"))
tree.insert(parent='', index=1, tags=1, values=(2, "タイトル２", "書いた人２", "説明２", "ページ数２", "サムネ２"))
tree.tag_configure(1,background = "#CCFFFF")
tree.insert(parent='', index=2, tags=2, values=(3, "タイトル３", "書いた人３", "説明３", "ページ数３", "サムネ３"))
tree.insert(parent='', index=3, tags=3, values=(4, "タイトル４", "書いた人４", "説明４", "ページ数４", "サムネ４"))
tree.tag_configure(3,background = "#CCFFFF") # 本来はAPIの取得結果の繰り返し文内で設定

一覧背景色の設定例
i=0
for ~
    # tagが奇数か偶数か判定
    if i & 1:
        # tagが奇数(レコードは偶数)の場合のみ、背景色の設定
        tree.tag_configure(i,background="#CCFFFF")
    i+=1
'''
# スクロールバーの追加(出来ていない)
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
# 一覧の表示位置設定
tree.place(x = 20, y = 40)

# トップレベルウィンドウを表示
root.mainloop()
