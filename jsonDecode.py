import json
import searchApi
from typing import List

class JsonDecode:
    def json_decode(self, searchWord):
        print("jsonDecodeStart")
        print("検索キーワード：" + searchWord + "：終わり")

        mylist = list()

        # 検索キーワードに文字列があるか判定
        if len(searchWord.strip()) > 0:
            print("検索キーワードあり！")
            # 本来は検索キーワードを元に書籍検索APIを呼ぶが、一時的にファイルから読み込みを行う
            #json_open = open('./sampleJson/testBookSearch3.json')
            bsa = searchApi.Search()
            json_open = bsa.bookSearchApi(searchWord)
            # ファイルから読み込み時はjson.loadにするが、API実行時はjson.loadsでないとエラーが発生する
            json_load = json.loads(json_open)
            #json_load = json.load(json_open)
            #print(json_load)
            book_items = json_load['items']
            
            countNo = 1
            for i in book_items:
                book_volumeInfo = i["volumeInfo"]
                
                # タイトルキーがあるか判定
                if "title" in book_volumeInfo:
                    bookTitle = book_volumeInfo["title"]
                else:
                    bookTitle = "---タイトルなし---"

                # 著者キーがあるか判定
                if "authors" in book_volumeInfo:
                    bookAuthors = ','.join(book_volumeInfo["authors"])
                else:
                    bookAuthors = "---著者なし---"
                
                # 説明文キーがあるか判定
                if "description" in book_volumeInfo:
                    bookDescription = book_volumeInfo["description"]
                    bookDescriptionExistence = book_volumeInfo["description"][:30] + "..."
                else:
                    bookDescription = "---説明分なし---"
                    bookDescriptionExistence = "---説明分なし---"
                
                # ページ数キーがあるか判定
                if "pageCount" in book_volumeInfo:
                    bookPageCount = str(book_volumeInfo["pageCount"]) + "ページ"
                else:
                    bookPageCount = "---ページ数なし---"
                
                # サムネイルキーがあるか判定
                if "imageLinks" in book_volumeInfo:
                    book_thumbnail = book_volumeInfo["imageLinks"]
                    if "thumbnail" in book_thumbnail:
                        thumbnailExistence = "サムネイルあり"
                        thumbnailUrl = book_thumbnail["thumbnail"]
                    else:
                        thumbnailExistence = "サムネイルなし"
                        thumbnailUrl = ""
                else:
                    thumbnailExistence = "サムネイルなし"
                    thumbnailUrl = ""
                #print("------------------------------------------")

                # Jsonへ書き込み
                book_dict = {
                    'no': countNo,
                    'title':bookTitle,
                    'authors':bookAuthors,
                    'bookDescriptionExistence':bookDescriptionExistence,
                    'bookDescription':bookDescription,
                    'pageCount':bookPageCount,
                    'thumbnailExistence':thumbnailExistence,
                    'thumbnailUrl':thumbnailUrl

                }

                mylist.append(json.dumps(book_dict, ensure_ascii=False))
                #print("生成したJson:" + book_dict.get())

                # countNoをカウントアップ
                countNo+=1

        return mylist

'''
def main():
    print("START")
    JsonDecode.json_decode("test")
    print("END")

main()
'''