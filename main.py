from ORM.model import AppsLinks, AppsData, Categories, db
from crawler.farsroid import FarsroidDataCrawler, FarsroidLinkCrawler
from crawler.config import BASE_URL
import sys


def create_table():
    db.create_tables([AppsLinks, AppsData, Categories])


def create_categories():
    for category in sorted(Categories.CATEGORIES_APPS):
        Categories.save_category(category)


def show_links():
    print(
        f'all link count: {AppsLinks.show_count()}\n'
        f'all crawled count: {AppsLinks.show_count(True)}\n'
        f'all not crawled count: {AppsLinks.show_count(False)}\n'
        f'all app count in database: {AppsData.show_count()}'
    )


def show_app_from_category():
    Categories.show_information()


if __name__ == '__main__':
    create_table()
    create_categories()

    if sys.argv[1] == '-cl':
        crawler = FarsroidLinkCrawler(BASE_URL)
        crawler.run_crawler()

    elif sys.argv[1] == '-cd':
        crawler = FarsroidDataCrawler()
        crawler.run_crawler()

    elif sys.argv[1] == '-sca':
        show_links()
    elif sys.argv[1] == '-scg':
        show_app_from_category()
