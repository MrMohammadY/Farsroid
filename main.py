from ORM.app_model import AppLink, AppData, GameLink, GameData
from ORM.category_model import AppCategory, GameCategory
from crawler.config import GAME_BASE_URL, APP_BASE_URL
from crawler.farsroid import FarsroidLinkCrawler, FarsroidDataCrawler
import sys


def create_table():
    tables = (
        AppLink, GameLink, AppCategory, GameCategory, AppData, GameData
    )

    for table in tables:
        table.create_table()


def create_categories():
    AppCategory.save_categories()
    GameCategory.save_categories()


def show_links():
    print(
        f'all link count: {AppLink.show_count()}\n'
        f'all crawled count: {AppLink.show_count(True)}\n'
        f'all not crawled count: {AppLink.show_count(False)}\n'
        f'all app count in database: {AppData.show_count()}'
    )


modes = {'game': GAME_BASE_URL, 'app': APP_BASE_URL}

if __name__ == '__main__':
    create_table()
    create_categories()

    if sys.argv[1] == '-cl':
        for mode, url in modes.items():
            crawler = FarsroidLinkCrawler(url, mode)
            crawler.run_crawler()

    elif sys.argv[1] == '-cd':
        for mode, url in modes.items():
            crawler = FarsroidDataCrawler(mode)
            crawler.run_crawler()

    elif sys.argv[1] == '-sai':
        AppCategory.show_information_category()
        GameCategory.show_information_category()
        show_links()
