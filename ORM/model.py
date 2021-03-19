from peewee import Model, CharField, ForeignKeyField, TextField, BooleanField
from playhouse.db_url import connect
from abc import abstractmethod

db = connect('mysql://Mohammad:09101916484@127.0.0.1:3306/Farsroid')


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    @abstractmethod
    def check_exists(cls, *args):
        pass


class AppsLinks(BaseModel):
    link = CharField(unique=TextField, max_length=255)
    crawl = BooleanField(default=False)

    @classmethod
    def show_count(cls, crawl=None):
        if crawl is None:
            return cls.select().count()
        if crawl is True:
            return cls.select().where(cls.crawl == True).count()
        if crawl is False:
            return cls.select().where(cls.crawl == False).count()

    @classmethod
    def load_links(cls):
        return cls.select().where(cls.crawl == False)

    @classmethod
    def check_exists(cls, link):
        query = cls.select().where(cls.link == link)
        if query.exists():
            return False
        return True

    @classmethod
    def save_links(cls, links):
        for link in links:
            if cls.check_exists(link):
                cls.create(link=link)

    @classmethod
    def update_status(cls, link):
        q_link = cls.select().where(cls.link == link).first()
        q_link.crawl = True
        q_link.save()


class Categories(BaseModel):
    name = CharField(max_length=255)

    CATEGORIES_APPS = [
        'اینترنت و شبکه',
        'مرورگر وب',
        'قفل کننده + مخفی ساز',
        'آرامش و تمرکز',
        'بهینه ساز',
        'آموزشی + درسی',
        'دوربین',
        'مبدل ویدئو و عکس',
        'ویرایش عکس',
        'دیکشنری',
        'ضبط صدا',
        'آفیس',
        'اشتراک گذاری فایل',
        'رادیو موزیک و تلویزیون',
        'آنتی ویروس + فایروال',
        'ویرایش ویدئو',
        'موزیک پلیر',
        'ویرایش موزیک',
        'ویدئو پلیر',
        'ابزارها',
        'کاربردی',
        'صفحه کلید',
        'اینترنت و شبکه',
        'مسنجر',
        'بارکدخوان - Scanner',
        'برنامه های پیشنهادی',
        'پزشکی و سلامت',
        'پرورش اندام',
        'پشتیبان گیری و بازیابی',
        'تقویم و یادآور',
        'ساعت زنگدار',
        'تماس، مخاطب و SMS',
        'سرگرمی',
        'ضبط صفحه نمایش',
        'فارسی',
        'کتاب خوان',
        'ماشین حساب+تبدیل واحد',
        'مدیریت ایمیل',
        'مدیریت دانلود',
        'مدیریت رمز عبور',
        'مدیریت فایل',
        'مدیریتی',
        'مذهبی',
        'موقعیت یاب و GPS',
        'همراه بانک',
        'وضعیت آب و هوا',
        'یادداشت برداری',
        'لانچر و شخصی سازی',
        'لاک اسکرین',
        'والپیپر',
        'تم - theme',
        'ویجت',
        'آیکون پک',
        'برنامه اندروید'
    ]

    @classmethod
    def check_exists(cls, category):
        query = cls.select().where(cls.name == category)
        if query.exists():
            return False
        return True

    @classmethod
    def save_category(cls, category):
        if cls.check_exists(category):
            cls.create(name=category)

    @classmethod
    def set_foreignkey_category(cls, category):
        if category in cls.CATEGORIES_APPS:
            q_category = cls.select().where(cls.name == category)
            return q_category
        return None

    @classmethod
    def show_information(cls):
        count = 0
        for category in sorted(cls.CATEGORIES_APPS):
            cat = cls.select().where(cls.name == category).first()
            print(f'category: {cat.name.ljust(40)}\t|\t'
                  f' app count: {cat.apps.count()}')
            count += cat.apps.count()
        print(count)


class AppsData(BaseModel):
    link = CharField(max_length=255)
    name = CharField(max_length=255)
    image = TextField()
    download_links = TextField()
    information = TextField()
    category = ForeignKeyField(Categories, backref='apps')

    @classmethod
    def check_exists(cls, link):
        query = cls.select().where(cls.link == link)
        if query.exists():
            return False
        return True

    @classmethod
    def save_app(cls, app):
        if cls.check_exists(app['link']):
            category = Categories.set_foreignkey_category(
                app['information'][3]).first()
            if category is not None:
                cls.create(
                    link=app['link'],
                    name=app['name'],
                    image=app['image'],
                    download_links=app['download_links'],
                    information=app['information'],
                    category=category
                )
                AppsLinks.update_status(app['link'])
                print('saved')
            else:
                print(f'category not found: {app["link"]}')
        else:
            AppsLinks.update_status(app['link'])
            print('exists')

    @classmethod
    def show_count(cls):
        return cls.select().count()
