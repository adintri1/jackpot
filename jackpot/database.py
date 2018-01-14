import psycopg2
from psycopg2.extras import RealDictCursor
import traceback
from urllib.parse import uses_netloc, urlparse
import pprint
import os

uses_netloc.append("postgres")
url = urlparse(os.environ["DATABASE_URL"]) # Export your postgres database url as an environment variable before this step

conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                        port=url.port)

conn.autocommit = True

cursor = conn.cursor(cursor_factory=RealDictCursor)


class Jackpotdb:

    def __init__(self):
        self.name = "jackpotdb"
        self.default_order = "scrapeddate"

    def get_rows(self):
        rows = []
        try:
            query = f"SELECT * FROM {self.name}"
            cursor.execute(query)
            rows = cursor.fetchall()
        except:
            print("error during select: " + str(traceback.format_exc()))
        return rows

    def show_records(self):
        rows = self.get_rows()
        for row in rows:
            pprint.pprint(row)

    def get_latest_lucky_combination(self, game_name):
        try:
            query = f"SELECT lucky_combination FROM {self.name} WHERE game = '{game_name}' " \
                    f"ORDER BY {self.default_order} DESC LIMIT 1;"
            cursor.execute(query)
            row = cursor.fetchall()
        except:
            print("error during select: " + str(traceback.format_exc()))
        return row

    def get_latest_extras(self, game_name):
        try:
            query = f"SELECT extras FROM {self.name} WHERE game = '{game_name}' " \
                    f"ORDER BY {self.default_order} DESC LIMIT 1;"
            cursor.execute(query)
            row = cursor.fetchall()
        except:
            print("error during select: " + str(traceback.format_exc()))
        return row

    def save_record(self, game):
        try:
            query = f"INSERT into {self.name} values(DEFAULT, " \
                    f"'{game.name}' , " \
                    f"'{game.lucky_combination}' , " \
                    f"'{game.extras}' , " \
                    f"CURRENT_TIMESTAMP);"
            cursor.execute(query)
        except:
            print("error during insert: " + str(traceback.format_exc()))

    def wipe_db(self):
        try:
            query = f"TRUNCATE {self.name} RESTART IDENTITY;"
            cursor.execute(query)
        except:
            print("error during select: " + str(traceback.format_exc()))
