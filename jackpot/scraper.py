from jackpot.utils import GameScraper, GameFactory
from jackpot.database import Jackpotdb

scraper = GameScraper()
db = Jackpotdb()

for name in GameFactory.game_names:
    game = GameFactory.get_game(name)
    scraper.set_url(game.name)
    scraper.get_html()
    game.set_lucky_combination(scraper.get_lucky_combination())
    if game.has_extras:
        game.set_extras(scraper.get_extras(game.extras_scrap_info))
    db.save_record(game)