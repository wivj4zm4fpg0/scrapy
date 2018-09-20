#news.pyが収集したデータを格納するためのクラスが定義されているファイル
#このクラスは「Page()」で初期化してdictのように使うことができるが、使えるキーがtitle,url,headline,lenght,indexのみである
from scrapy.item import Item, Field

class Page(Item):
	title = Field()
	url = Field()
	headline = Field()
	length = Field()
	index = Field()

