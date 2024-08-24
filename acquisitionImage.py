# HTTPリクエスト用のrequestsはインストール必要
import requests
import os
import glob
# 画像処理ライブラリのPILはインストール必要
from PIL import Image

class WebImage:
    def acquisitionThumbnail(self, url):
        picturePass = ''
        # サムネ用URL存在確認
        if not url:
            # URLがない場合
            # 元々用意している画像パスを返却
            picturePass = './temp/noImage.jpg'
        else:
            # URLがある場合
            # 保存したサムネ画像があれば削除
            for p in glob.glob('./temp/thumbnail.jpg', recursive=True):
                if os.path.isfile(p):
                    os.remove(p)
            
            print("取得対象URL：" + url)
            # サムネイル用取得APIを実行
            request = requests.get(url, stream=True)
            # リクエスト結果のサムネイル画像を取得
            image = Image.open(request.raw).convert('RGB')
            # 取得したサムネ画像をローカルへ保存
            image.save('./temp/thumbnail.jpg')
            picturePass = './temp/thumbnail.jpg'
        
        # サムネ画像のパスを返却
        return picturePass
