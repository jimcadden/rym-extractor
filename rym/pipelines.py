from scrapy.exceptions import DropItem


class CleanData(object):
  def process_item(self, item, spider):
    for key,val in item.iteritems():
      if val is not None:
        if isinstance(val, basestring):
          item[key] = item[key].strip()
        elif type(val) is list:
          if len(val) == 1:
            item[key] = ''.join(val)
          else:
            item[key] = ', '.join(val)
    item['release_date'] = item['release_date'].replace(',','')
    return item

class StringToInt(object):
  def process_item(self, item, spider):
    keys = ['rank_year','rank_overall','rating', 'release_year','votes', 'chart_position']
    for i, key in enumerate(keys):
      if key in item and len(item[key]) > 0:
        if key == 'rating':
          item[key] = float(item[key]) 
        else:
          item[key] = int(item[key].replace(',', '')) 
    return item
