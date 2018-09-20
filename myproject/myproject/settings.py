#クローラーの設定ファイル
DOWNLOAD_DELAY = 3#ここでサイトへのサクセス間隔を3秒に設定している

BOT_NAME = 'myproject'

SPIDER_MODULES = ['myproject.spiders']
NEWSPIDER_MODULE = 'myproject.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'myproject.pipelines.MongoPipeline': 800
}

