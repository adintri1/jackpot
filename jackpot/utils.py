import sys
import requests
import json
from requests import Timeout, HTTPError, TooManyRedirects
from requests.exceptions import SSLError
from bs4 import BeautifulSoup


class Game:

    def __init__(self, name):
        self.name = name
        self.has_extras = False
        self.lucky_combination = None
        self.extras = None
        self.extras_scrap_info = {}

    def set_lucky_combination(self, combination):
        self.lucky_combination = combination

    def set_extras(self, extras):
        self.extras = extras


class GameFactory(object):

    game_names = ('la-primitiva', 'euromillones', 'bonoloto', 'gordo-primitiva')

    @staticmethod
    def get_game(game_name):
        if game_name == GameFactory.game_names[0]:
            return Primitiva(game_name)
        elif game_name == GameFactory.game_names[1]:
            return Euromillones(game_name)
        elif game_name == GameFactory.game_names[2]:
            return Bonoloto(game_name)
        elif game_name == GameFactory.game_names[3]:
            return Gordo(game_name)


class Primitiva(Game):

    def __init__(self, name):
        Game.__init__(self, name)
        self.has_extras = True
        self.extras_scrap_info = {'Bonus Number': 'span', 'Refund': 'span'}


class Euromillones(Game):

    def __init__(self, name):
        Game.__init__(self, name)
        self.has_extras = True
        self.extras_scrap_info = {'Lucky Stars:': 'ul'}


class Bonoloto(Game):

    def __init__(self, name):
        Game.__init__(self, name)
        self.has_extras = True
        self.extras_scrap_info = {'Bonus Number': 'span', 'Refund': 'span'}


class Gordo(Game):

    def __init__(self, name):
        Game.__init__(self, name)
        self.has_extras = True
        self.extras_scrap_info = {'Refund': 'span'}


class GameScraper:

    def __init__(self):
        self.base_url = "https://www.loteriasyapuestas.es/en/"
        self.page_url = None
        self.page_html = None
        self.timeout = 3.05

    def set_url(self, game_name):
        self.page_url = f"{self.base_url}{game_name}"

    def get_html(self):
        try:
            s = requests.Session()
            page = s.get(self.page_url, timeout=self.timeout)
            self.page_html = BeautifulSoup(page.text, "html.parser")

        except ConnectionError as err:
            print("ConnectionError: {0}".format(err))
        except Timeout as err:
            print("TimeoutError: {0}".format(err))
        except HTTPError as err:
            print("HTTPError: {0}".format(err))
        except TooManyRedirects as err:
            print("TooManyRedirects: {0}".format(err))
        except SSLError as err:
            print("SSLError: {0}".format(err))
        except TypeError as err:
            print("TypeError: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])

            return self.page_html

    def get_content(self, target, sibling):
        content = self.page_html.find("p", string=target).find_next_sibling(sibling)
        if content is None:
            return "Not found"
        else:
            return ' '.join(content.text.split())

    def get_lucky_combination(self):
        combination = self.get_content("Lucky combination", "ul")
        return json.dumps(combination.split())

    def get_extras(self, scrap_info):
        extras_list = []
        for k, v in scrap_info.items():
            extra = self.get_content(k, v)
            t = {k: extra}
            extras_list.append(t)

        return json.dumps(extras_list)
