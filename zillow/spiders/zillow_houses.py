# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..utils import URL, cookie_parser, parse_new_url
from ..items import ZillowItem
import json
cookie_string = 'zguid=23|%244b152902-5742-43a9-b447-07d6005d39a7; _ga=GA1.2.1870745959.1620808032; zjs_user_id=null; zjs_anonymous_id=%224b152902-5742-43a9-b447-07d6005d39a7%22; _gcl_au=1.1.1812764233.1620808032; __pdst=6ebd80eed6494503befdb32519a8de27; _pxvid=d9b495ac-b2fb-11eb-bac0-0242ac120010; _pin_unauth=dWlkPU5qWmpZVFk0TTJZdE5EVmtNQzAwWVRNMExUZzNPV1l0WlRJek1HRTFZMlk0T0dJMw; G_ENABLED_IDPS=google; zgsession=1|e1a19d45-c739-4765-80d0-15bcdb37198b; DoubleClickSession=true; _gid=GA1.2.1090420437.1621355476; KruxPixel=true; _derived_epik=dj0yJnU9QXhSMmtyd1lsZUU2c25mOS1KSVdhZ1h5MFlwNEVVSVEmbj1QblFlS05iaE5jcFlEQjcxc2tTQ3F3Jm09ZiZ0PUFBQUFBR0NqNjlRJnJtPWYmcnQ9QUFBQUFHQ2o2OVE; JSESSIONID=794A0C243CF7A37A99F1ED807256E6D5; utag_main=v_id:01795fafe141001dc5eab699cd7003072001706a00bd0$_sn:4$_se:1$_ss:1$_st:1621357276239$dc_visit:4$ses_id:1621355476239%3Bexp-session$_pn:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_event:1%3Bexp-session$dc_region:eu-central-1%3Bexp-session; _px3=c124b4f1864fa446069792884e2bb59f8105bdabe48ea35fd5df9d5c7726718d:DR5/wE3naRI4lZyjaTbhsccknKzEjx7Hiwqujojomnsx6JOucv3jyV7eRAeDMvX2qLftjTT5qOdRw6z4I4o/pg==:1000:Rz8b460sFMRgv3ioOJZKgT3HLKpKnfi1zeiJwmqk1Q52tgkt9LNu++3MV2StjyEF4uXWC9uTXiUswWLaxp9qTbsp09aMUHN/qQw40qVRu8m0OSCzSVxYEiEaO9BvgDeyg+bo/e8s+shWAM3yK+N9CJXGwUUVViaySVbVyj8YqMdzKvngdE2U77e25/oRty67Xx4zKo1MQKfnyGf/BAvV9Q==; _uetsid=77a4ff20b7f611ebb3d3fd66da995f92; _uetvid=d9ca5b40b2fb11eb9bff0565b289fd4f; KruxAddition=true; AWSALB=ugE/C9I43pYmyeWuGTeWmUJ2neGRgLf96bRvuiV3Lg8BoIrjdeL7fUVCcttuqAkjIF4Pk2xxYeFLCB/kvatQpYV2ki9FjmFLKh25cHpNovBYm0AwDUVhk69hqR1Q; AWSALBCORS=ugE/C9I43pYmyeWuGTeWmUJ2neGRgLf96bRvuiV3Lg8BoIrjdeL7fUVCcttuqAkjIF4Pk2xxYeFLCB/kvatQpYV2ki9FjmFLKh25cHpNovBYm0AwDUVhk69hqR1Q; search=6|1623947584875%7Crect%3D41.16230754440855%252C-73.00442580179886%252C40.327897953603156%252C-74.61117629008011%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D4%26sort%3Ddays%26z%3D1%26price%3D0-615813%26mp%3D0-2000%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%096181%09%09%09%09%09%09; _gat=1'


class ZillowHousesSpider(scrapy.Spider):
    name = 'zillow_houses'
    allowed_domains = ['www.zillow.com']

    def start_requests(self):
        yield scrapy.Request(
            url=URL,
            callback=self.parse,
            cookies=cookie_parser(cookie_string),
            meta={
                'currentPage': 1
            }
        )

    def parse(self, response):
        current_page = response.meta['currentPage']
        json_resp = json.loads(response.body)
        print('*'*100)
        print(json_resp['cat1'])
        houses = json_resp.get('cat1').get('searchResults').get('listResults')
        for house in houses:
            loader = ItemLoader(item=ZillowItem())
            loader.add_value('id', house.get('id'))
            loader.add_value('img_source', house.get('imgSrc'))
            loader.add_value('detail_url', house.get('detailUrl'))
            loader.add_value('status_type', house.get('statusType'))
            loader.add_value('status_text', house.get('statusText'))
            loader.add_value('price', house.get('price'))
            loader.add_value('address', house.get('address'))
            loader.add_value('beds', house.get('beds'))
            loader.add_value('baths', house.get('baths'))
            loader.add_value('area_sqfl', house.get('area'))
            loader.add_value('latitude', house.get('latLong').get('latitude'))
            loader.add_value('longitude', house.get('latLong').get('longitude'))
            loader.add_value('broker_name', house.get('brokerName'))
            loader.add_value('broker_phone', house.get('brokerPhone'))
            yield loader.load_item()

        total_pages = json_resp.get('cat1').get('searchList').get('totalPages')
        if current_page <= total_pages:
            current_page+=1
            yield scrapy.Request(
                url=parse_new_url(URL, current_page),
                callback=self.parse,
                cookies=cookie_parser(cookie_string),
                meta={
                    'currentPage': current_page
                }
            )

