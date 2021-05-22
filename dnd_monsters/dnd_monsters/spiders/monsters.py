import scrapy


# links = //a[@class="row-link"]/@href
CREATURES_LINKS = '//a[@class="row-link"]/@href'
# next pag3e = //a[contains(@class, "page-link") and @rel="next"]/@href
NEXT_PAGE_BTN = '//a[contains(@class, "page-link") and @rel="next"]/@href'
# name = //h1[@class="content-header-title mb-0"]/text() (without \n)
CREATURE_NAME = '//h1[@class="content-header-title mb-0"]/text()'
# table = //div[@class="article-2-columns"]/p/node()/text()
CREATURE_BASIC_DATA = '//div[@class="article-2-columns"]/p/node()/text()'
# caracteristicas = //table[@class="table table-xs"]//th/text() (names)
CREATURE_TABLE_NAMES = '//table[@class="table table-xs"]//th/text()'
# pts caracteristicas = //table[@class="table table-xs"]//td/span/text() (STATS)
CREATURE_TABLE_VALUES = '//table[@class="table table-xs"]//td/span/text()'
# habilidades = //div[@class="article-2-columns"]/p[2]/node()/text()
CREATURE_COMPETENCES = '//div[@class="article-2-columns"]/p[2]/node()/text()'
# all stats = //div[@class="article-2-columns"]/div/node()/text()
CREATURE_ALL_STATS = '//div[@class="article-2-columns"]/div/node()/text()'


class monstersSpider(scrapy.Spider):
    name = 'monsters'
    start_urls = [
        'https://dungeon20.com/games/dnd-5/creatures'
    ]
    custom_settings = {
        'FEEDS': {
            'monsters.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'indent': 4
            }
        }
    }

    def parse_monster(self, response, **kwargs):
        monster_link = kwargs['url']
        monster_name = response.xpath(CREATURE_NAME).get().replace('\n', '')
        # monster_basic = response.xpath(CREATURE_BASIC_DATA).getall()
        monster_table_names = response.xpath(CREATURE_TABLE_NAMES).getall()
        monster_table_values = response.xpath(CREATURE_TABLE_VALUES).getall()
        monster_table = {f'{table}': monster_table_values[i]
                         for i, table in enumerate(monster_table_names)}
        yield {
            'name': monster_name,
            # 'basics': monster_basic,
            'table': monster_table,
            'link': monster_link
        }

    def parse(self, response):
        links = response.xpath(CREATURES_LINKS).getall()
        next_page = response.xpath(NEXT_PAGE_BTN).get()
        for link in links:
            yield response.follow(link, callback=self.parse_monster, cb_kwargs={'url': response.urljoin(link)})
        if next_page:
            yield response.follow(next_page, callback=self.parse)


# Debo hacer que busque en las siguientes paginas, ademas de terminar de mostrar los datos por monstruo y corregir el error al enseñar los datos de
# monster_basic. Evaluar utilizar un archivo para cada monstruo (requiere estudio online)
# json.maxItemsComputed
