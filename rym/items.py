from scrapy.item import Item, Field


class Album(Item):
    artist = Field()
    cover_art = Field()
    descriptors = Field()
    genres= Field()
    media = Field()
    ranks = Field()
    rating = Field()
    recorded = Field()
    release_date = Field()
    release_year = Field()
    subgenres = Field()
    title = Field()
    url = Field()
    votes = Field()
    # TODO:
    # issues
    # reviews 

class ChartRow(Album):
    chart_position = Field()
    cover_art_icon = Field()
    title_url = Field()
