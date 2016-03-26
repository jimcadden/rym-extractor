from scrapy.item import Item, Field

class Album(Item):
    artist = Field()
    cover_art = Field()
    descriptors = Field()
    genres= Field()
    media = Field()
    rank_year = Field()
    rank_overall = Field()
    rating = Field()
    recorded = Field()
    release_date = Field()
    release_year = Field()
    release_DOY = Field()
    subgenres = Field()
    title = Field()
    url = Field()
    votes = Field()

class ChartRow(Album):
    chart_position = Field()
    cover_art_icon = Field()
    title_url = Field()
