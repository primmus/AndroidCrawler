# coding = utf-8


import sys

reload(sys)
sys.setdefaultencoding('utf8')

class CommonSpider(Spider):
    """

    """

    table_name = None
    market_name = None

    def __init__(self, spider_name, market_name, table_name, *a, **kw):
        super(CommonSpider, self).__init__(*a, **kw)


