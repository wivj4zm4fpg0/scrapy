#クローラーを起動した時最初にopen_spiderが呼び出される。クローラーを終了した時にclose_spiderが呼び出される。new.pyが収集したデータをyieldした時process_itemが呼び出され、データベースにデータを保存する
from pymongo import MongoClient

class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['WebInfoSys']
        self.collection = self.db['pages']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        titles = []
        for entry in self.collection.find():
            titles.append(entry['title'])
        if item['title'] not in titles:
            self.collection.insert_one(dict(item))

