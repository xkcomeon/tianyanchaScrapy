# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from .model import Model, get_sqlsession, engine, create_newtable
from .mongodb import MongoHandler

class TianyanchascrapyPipeline(object):
    def __init__(self):
        self.session = get_sqlsession(engine)
        create_newtable(engine)

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        _item = Model.db_distinct(self.session, Model, item, item['url'])
        Model.save_mode(self.session, Model(), _item)
        return _item


class TianyanchascrapyPipelineMongo:
    def __init__(self):
        self.mongo = MongoHandler(conn_uri='localhost', db='spider', collection_name='tianyancha')

    def close_spider(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        self.mongo.run(item)
        return item


