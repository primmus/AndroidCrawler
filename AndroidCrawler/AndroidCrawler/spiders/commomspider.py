# coding = utf-8


import sys

reload(sys)
sys.setdefaultencoding('utf8')

class CommonSpider(Spider):
    name = 'commonspider'

    def __init__(self, name, table_name, *args, **kwargs):
        super(CommonSpider, self).__init__(*args, **kwargs)
        