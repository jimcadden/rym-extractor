from scrapy.exceptions import DropItem
import datetime


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
    if item['release_date'] is not None:
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

class DayOfYear(object):
  def process_item(self, item, spider):
    # Assumes item data is cleaned & strings converted to ints 
    # release_date string may be: None, "January", "January 30"
    month = 1
    day = 1
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    if item['release_date'] is not None:
      parts = item['release_date'].split(' ')
      month = months.index(parts[0]) + 1
      if len(parts) == 2:
        day = int(parts[1])
    item['release_DOY'] = datetime.date(item['release_year'], month, day).timetuple().tm_yday
    return item
