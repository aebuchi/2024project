# HTTPリクエスト用のrequestsはインストール必要
import requests

# 他の検索方法もあるがオーソドックスのみでとりあえず(改良の余地あり)
bookSearchUrl = 'https://www.googleapis.com/books/v1/volumes?q='

class Search:
    def bookSearchApi(self, keyWord):
    #def bookSearchApi(keyWord): このクラスのみ実行用
        book_json = ''
        # キーワード存在確認
        # キーワードがない場合は、中身なしのJsonを
        if not keyWord:
            # キーワードがない場合
            # 空文字を返却
            book_json = ''
        else:
            # キーワードがある場合
            print("書籍取得対象キーワード：" + keyWord)
            # 書籍検索APIを実行(10行分しか取得できない気がする)
            response = requests.get(bookSearchUrl + keyWord.strip(), stream=True)

            book_json = response.text.replace("'", "").replace("\n", "")
        # 取得した書籍のJsonを返却
        return book_json

'''
def main():
    print("START")
    Search.bookSearchApi("戦闘妖精")
    print("END")

main()
'''