from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode
import json

URL='https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.61117629008011%2C%22east%22%3A-73.00442580179886%2C%22south%22%3A40.327897953603156%2C%22north%22%3A41.16230754440855%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A615813%7D%2C%22monthlyPayment%22%3A%7B%22min%22%3A0%2C%22max%22%3A2000%7D%2C%22isPreMarketForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isPreMarketPreForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D&wants={%22cat1%22:[%22listResults%22],%22cat2%22:[%22total%22]}'


def cookie_parser(cookie_string):
    cookie=SimpleCookie()
    cookie.load(cookie_string)
    cookies = {}

    for key, morsel in cookie.items():
        cookies[key] = morsel.value

    return cookies

def parse_new_url(url, page_number):
    url_parsed = urlparse(url)
    query_string = parse_qs(url_parsed.query)
    search_query_state = json.loads(query_string.get('searchQueryState')[0])
    search_query_state['pagination'] = {"currentPage": page_number}
    query_string.get('searchQueryState')[0] = search_query_state
    encodet_qs = urlencode(query_string, doseq=True)
    new_url = f'https://www.zillow.com/search/GetSearchPageState.htm?{encodet_qs}'
    return new_url




