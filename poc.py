from scrapy.crawler import CrawlerProcess
from rym.s.album import AlbumSpider

spider = AlbumSpider()
process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
      })
process.crawl(spider)
process.start()
