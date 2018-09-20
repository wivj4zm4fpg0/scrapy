#クライアントプログラムである
from pymongo import MongoClient
import operator, MeCab

#出力するためのページを格納するためのクラス
class Page():
    def __init__(self, title='', url='', length=0, headline='', score=0):
        self._title = title
        self._url = url
        self._length = length
        self._headline = headline
        self._score = score

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def length(self):
        return self._length

    @property
    def headline(self):
        return self._headline

    @property
    def score(self):
        return self._score

#ユーザが入力した文字列で情報検索システムを使用する関数
def search(query=''):
    pageList = []
    pages = MongoClient().WebInfoSys.pages
    tagger = MeCab.Tagger()
    tagger.parse('')
    for entry in pages.find():
        score = 0
        node = tagger.parseToNode(query)
        flag = False
        while node:
            if node.surface in entry['index']:
                flag = True
                score += entry['index'][node.surface] * 1000
            node = node.next
        if flag:
            score /= entry['length']
            pageList.append(Page(title=entry['title'], url=entry['url'], headline=entry['headline'], score=score, length=entry['length']))
    pageList.sort(reverse=True, key=operator.attrgetter('score'))
    count = 0
    print('-------------------------------------------')
    for entry in pageList:
        print('タイトル = ' + entry.title)
        print('URL = ' + entry.url)
        print('ヘッダー = ' + entry.headline)
        print('単語の数 = ' + str(entry.length))
        print('スコア = ' + str(entry.score))
        print('-------------------------------------------')
        count += 1
        if count == 20:
            break
        if count % 5 == 0:
            input('続きを読むにはEnter')
            print()

#ここが最初に実行される
if __name__ == '__main__':
    search(input('文字を入力してください：'))

