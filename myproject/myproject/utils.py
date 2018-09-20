#HTMLを解析して主要な文章を抜き出し、その文章を返すための関数が実装されているファイル
import logging
import lxml.html
import readability

logging.getLogger('readability.readability').setLevel(logging.WARNING)

def get_content(html):#htmlは解析されるHTML文書である
    document = readability.Document(html)
    content_html = document.summary()
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    return content_text
