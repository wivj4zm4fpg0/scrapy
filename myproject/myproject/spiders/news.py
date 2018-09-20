#クローラーの本体である。myprojectより下のディレクトリで「scrapy crawl news」とコマンドを打つことにより実行できる。
import requests, re, MeCab, scrapy
from bs4 import BeautifulSoup
from myproject.items import Page
from myproject.utils import get_content

class NewsSpider(scrapy.Spider):
    name = 'news'#クローラーの名前である。「scrapy crawl ○○」の○○に当たる部分である。
    
    #アクセスするドメインを限定する
    allowed_domains = ['news.yahoo.co.jp', 'headlines.yahoo.co.jp', 'www3.nhk.or.jp', 'feeds.cnn.co.jp', 'www.cnn.co.jp', 'feeds.bbci.co.uk', 'www.bbc.com']

    #クローラーが使うURLを定義している。
    start_urls = ['https://news.yahoo.co.jp/pickup/rss.xml', 'https://www3.nhk.or.jp/rss/news/cat0.xml', 'http://feeds.cnn.co.jp/rss/cnn/cnn.rdf', 'http://feeds.bbci.co.uk/japanese/rss.xml']

    #クローラーを起動するとNewsSpiderのインスタンスが作られ、このメソッドを実行する。
    def parse(self, response):
        if response.url == 'https://news.yahoo.co.jp/pickup/rss.xml':
            for url in response.css('item > link::text').extract():
                yield scrapy.Request(response.urljoin(url), self.parse_yahoo)

        elif response.url == 'https://www3.nhk.or.jp/rss/news/cat0.xml':
            for url in response.css('item > link::text').extract():
                yield scrapy.Request(response.urljoin(url), self.parse_nhk)

        elif response.url == 'http://feeds.cnn.co.jp/rss/cnn/cnn.rdf':
            r = requests.get(response.url)
            bs = BeautifulSoup(r.content)
            for url in bs.select('a'):
                yield scrapy.Request(response.urljoin(url.get('href')), self.parse_cnn)

        elif response.url == 'http://feeds.bbci.co.uk/japanese/rss.xml':
            for url in response.css('item > link::text').extract():
                yield scrapy.Request(response.urljoin(url), self.parse_bbs)

    #Yahoo!ニュースからデータを収集するメソッド
    def parse_yahoo(self, response):
        item = Page()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        url = response.css('a.newsLink::attr("href")').extract_first()
        r = requests.get(url)
        content = re.sub(r'\n|\u3000', '', get_content(r.content))
        item['headline'] = content[:100] + '…'
        tagger = MeCab.Tagger()
        tagger.parse('')
        node = tagger.parseToNode(content)
        length = -2
        index = {}
        while node:
            if '$' not in node.surface and '.' not in node.surface:
                length += 1
                if node.surface in index:
                    index[node.surface] += 1
                else:
                    index[node.surface] = 1
            node = node.next
        item['length'] = length
        item['index'] = index
        yield item

    #NHK NEWS WEBからデータを収集するメソッド
    def parse_nhk(self, response):
        item = Page()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        content = re.sub(r'\n|\r|\t', '', get_content(response.text))
        item['headline'] = content[:100] + '…'
        tagger = MeCab.Tagger()
        tagger.parse('')
        node = tagger.parseToNode(content)
        length = -2
        index = {}
        while node:
            if '$' not in node.surface and '.' not in node.surface:
                length += 1
                if node.surface in index:
                    index[node.surface] += 1
                else:
                    index[node.surface] = 1
            node = node.next
        item['length'] = length
        item['index'] = index
        yield item

    #CNN.co.jpからデータを収集するメソッド
    def parse_cnn(self, response):
        item = Page()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        content = re.sub(r'\r|\n|\xa0| ', '', get_content(response.text))
        item['headline'] = content[:100] + '…'
        tagger = MeCab.Tagger()
        tagger.parse('')
        node = tagger.parseToNode(content)
        length = -2
        index = {}
        while node:
            if '$' not in node.surface and '.' not in node.surface:
                length += 1
                if node.surface in index:
                    index[node.surface] += 1
                else:
                    index[node.surface] = 1
            node = node.next
        item['length'] = length
        item['index'] = index
        yield item

    #BBS NEWSからデータを収集するメソッド
    def parse_bbs(self, response):
        item = Page()
        item['title'] = response.css('title::text').extract_first()
        item['url'] = response.url
        content = re.sub(r'\n| |\u3000', '', get_content(response.text))
        item['headline'] = content[:100] + '…'
        tagger = MeCab.Tagger()
        tagger.parse('')
        node = tagger.parseToNode(content)
        length = -2
        index = {}
        while node:
            if '$' not in node.surface and '.' not in node.surface:
                length += 1
                if node.surface in index:
                    index[node.surface] += 1
                else:
                    index[node.surface] = 1
            node = node.next
        item['length'] = length
        item['index'] = index
        yield item
