# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json

class DemospiderPipeline(object):
    def process_item(self, item, spider):
        with open('url.txt', 'a') as urlf:
            urlf.write(item['image_url'] + "\n")
        # 下载图片
        try:
            img = requests.get(item.image_url, timeout=10)
        except requests.exceptions.ConnectionError:
            print '【错误】当前图片无法下载'

        else:
            name = item.image_name.replace('/', '')
            local_save = 'D:\\PythonWorkSpace\\demoSpider\\pics\\' + name + '.jpg'
            with open(local_save, 'wb') as sf:
                sf.write(img.content)
        return item
