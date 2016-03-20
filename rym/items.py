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

class Artist(Item):
    albums_ep = Field()
    albums_live = Field()
    albums_single = Field()
    albums_studio = Field()
    formed = Field()
    genres = Field()
    members = Field()
    name = Field()
    url = Field()

#class Chart(Item):
#    length = Field()
#    parameters = Field()

class ChartRow(Item):
    artist = Field()
    artist_url = Field()
    cover_art = Field()
    genres= Field()
    position = Field()
    rating = Field()
    title = Field()
    title_url = Field()
    votes = Field()
    release_year = Field()
