from models.category_model import AppCategory, GameCategory
from models.base_model import BaseModel
from peewee import CharField, BooleanField, TextField, ForeignKeyField


class BaseLink(BaseModel):

    @classmethod
    def load_links(cls):
        # return all links from database which crawl = False
        return cls.select().where(cls.crawl == False)

    @classmethod
    def check_exists(cls, link):
        # if exists return True else return False
        query = cls.select().where(cls.link == link)
        if query.exists():
            return True
        return False

    @classmethod
    def save_links(cls, links):
        """
        give links and check exists each link, if that not exists save that
        :param links: list of links
        :return:
        """
        for link in links:
            if cls.check_exists(link) is False:
                cls.create(link=link)

    @classmethod
    def update_status(cls, link):
        # give link and change crawler to True
        query = cls.select().where(cls.link == link).first()
        query.crawl = True
        query.save()

    @classmethod
    def show_count(cls, crawl=None):
        if crawl is None:
            return cls.select().count()
        if crawl is True:
            return cls.select().where(cls.crawl == True).count()
        if crawl is False:
            return cls.select().where(cls.crawl == False).count()


class AppLink(BaseLink):
    link = CharField(max_length=255, unique=True)
    crawl = BooleanField(default=False)


class GameLink(BaseLink):
    link = CharField(max_length=255, unique=True)
    crawl = BooleanField(default=False)


class BaseData(BaseModel):
    link = CharField(max_length=255, unique=True)
    name = CharField(max_length=128)
    image = TextField()
    last_updated = CharField(max_length=64)
    price = CharField(max_length=64)
    version = CharField(max_length=64)
    download_links = TextField()

    @classmethod
    def check_exists(cls, link):
        query = cls.select().where(cls.link == link)
        if query.exists():
            return True
        return False

    @classmethod
    def update_app(cls, app):
        cls.update(**app).where(cls.link == app['link'])

    @classmethod
    def show_count(cls):
        return cls.select().count()


class AppData(BaseData):
    category = ForeignKeyField(AppCategory, backref='apps')

    @classmethod
    def save_app(cls, app):
        if cls.check_exists(app['link']) is False:
            category = AppCategory.set_foreignkey_category(app['category'])
            app['category'] = category

            if category is not None:

                cls.create(**app)

                AppLink.update_status(app['link'])
                print('saved...')

            else:
                print(f'category not found: {app["link"]}')

        else:

            AppLink.update_status(app['link'])
            cls.update_app(app)

            print('exists')


class GameData(BaseData):
    age = CharField(max_length=128, verbose_name='age')
    internet = CharField(max_length=128, verbose_name='internet')
    category = ForeignKeyField(GameCategory, related_name='games')

    @classmethod
    def save_app(cls, app):
        if cls.check_exists(app['link']) is False:
            category = GameCategory.set_foreignkey_category(app['category'])
            app['category'] = category

            if category is not None:

                cls.create(**app)

                GameLink.update_status(app['link'])
                print('saved...')

            else:
                print(f'category not found: {app["link"]}')

        else:

            GameLink.update_status(app['link'])
            cls.update_app(app)

            print('exists')
