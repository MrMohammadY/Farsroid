from models.base_model import BaseModel
from peewee import CharField


class BaseCategory(BaseModel):
    name_f = CharField(max_length=64, unique=True)
    name_e = CharField(max_length=64, unique=True)

    @classmethod
    def save_categories(cls):
        for category in cls.CATEGORIES:
            cls.get_or_create(**category)

    @classmethod
    def set_foreignkey_category(cls, category):
        for cat in cls.CATEGORIES:
            if category in cat['name_f']:
                query = cls.select().where(cls.name_f == category).first()
                return query
        return None


class AppCategory(BaseCategory):
    CATEGORIES = [
        {'name_e': 'antivirus firewall', 'name_f': 'آنتی ویروس + فایروال'},
        {'name_e': 'simulation', 'name_f': 'شبیه سازی'},
        {'name_e': 'lock and hide data', 'name_f': 'قفل کننده + مخفی ساز'},
        {'name_e': 'android program', 'name_f': 'برنامه اندروید'},
        {'name_e': 'relax and focus', 'name_f': 'آرامش و تمرکز'},
        {'name_e': 'android optimization', 'name_f': 'بهینه ساز'},
        {'name_e': 'education and curriculum', 'name_f': 'آموزشی + درسی'},
        {'name_e': 'camera', 'name_f': 'دوربین'},
        {'name_e': 'photo editor', 'name_f': 'ویرایش عکس'},
        {'name_e': 'photo and video converter', 'name_f': 'مبدل ویدئو و عکس'},
        {'name_e': 'video editor', 'name_f': 'ویرایش ویدئو'},
        {'name_e': 'music editor', 'name_f': 'ویرایش موزیک'},
        {'name_e': 'music players', 'name_f': 'موزیک پلیر'},
        {'name_e': 'video players', 'name_f': 'ویدئو پلیر'},
        {'name_e': 'radio music tv', 'name_f': 'رادیو موزیک و تلویزیون'},
        {'name_e': 'file transfer sharing', 'name_f': 'اشتراک گذاری فایل'},
        {'name_e': 'office', 'name_f': 'آفیس'},
        {'name_e': 'tools', 'name_f': 'ابزارها'},
        {'name_e': 'utility', 'name_f': 'کاربردی'},
        {'name_e': 'keyboard android', 'name_f': 'صفحه کلید'},
        {'name_e': 'internet and network', 'name_f': 'اینترنت و شبکه'},
        {'name_e': 'web browser', 'name_f': 'مرورگر وب'},
        {'name_e': 'messenger', 'name_f': 'مسنجر'},
        {'name_e': 'scanner', 'name_f': 'بارکدخوان - Scanner'},
        {'name_e': 'suggested apps', 'name_f': 'برنامه های پیشنهادی'},
        {'name_e': 'medicine and health', 'name_f': 'پزشکی و سلامت'},
        {'name_e': 'bodybuilding', 'name_f': 'پرورش اندام'},
        {'name_e': 'backup and restore', 'name_f': 'پشتیبان گیری و بازیابی'},
        {'name_e': 'calendar and reminder', 'name_f': 'تقویم و یادآور'},
        {'name_e': 'alarm clock', 'name_f': 'ساعت زنگدار'},
        {'name_e': 'call contact sms', 'name_f': 'تماس، مخاطب و SMS'},
        {'name_e': 'dictionary', 'name_f': 'دیکشنری'},
        {'name_e': 'fun', 'name_f': 'سرگرمی'},
        {'name_e': 'voice call recording', 'name_f': 'ضبط صدا'},
        {'name_e': 'screen recorder', 'name_f': 'ضبط صفحه نمایش'},
        {'name_e': 'persian', 'name_f': 'فارسی'},
        {'name_e': 'book reader', 'name_f': 'کتاب خوان'},
        {'name_e': 'calculator unit converter',
         'name_f': 'ماشین حساب+تبدیل واحد'},
        {'name_e': 'email management', 'name_f': 'مدیریت ایمیل'},
        {'name_e': 'download manager', 'name_f': 'مدیریت دانلود'},
        {'name_e': 'password manager', 'name_f': 'مدیریت رمز عبور'},
        {'name_e': 'file manager', 'name_f': 'مدیریت فایل'},
        {'name_e': 'management', 'name_f': 'مدیریتی'},
        {'name_e': 'religious', 'name_f': 'مذهبی'},
        {'name_e': 'gps', 'name_f': 'موقعیت یاب و GPS'},
        {'name_e': 'mobile bank android', 'name_f': 'همراه بانک'},
        {'name_e': 'weather', 'name_f': 'وضعیت آب و هوا'},
        {'name_e': 'notes app android', 'name_f': 'یادداشت برداری'},
        {'name_e': 'launcher', 'name_f': 'لانچر و شخصی سازی'},
        {'name_e': 'lock screen', 'name_f': 'لاک اسکرین'},
        {'name_e': 'wallpaper', 'name_f': 'والپیپر'},
        {'name_e': 'theme', 'name_f': 'تم - theme'},
        {'name_e': 'widget', 'name_f': 'ویجت'},
        {'name_e': 'icon pack', 'name_f': 'آیکون پک'},
    ]

    @classmethod
    def show_information_category(cls):
        count = 0

        for category in cls.CATEGORIES:
            cat = cls.select().where(cls.name_e == category['name_e']).first()

            print(
                f'category: {cat.name_e.ljust(40)} \t\t'
                f'persian name: {cat.name_f.ljust(40)}\t\t'
                f'app count: {cat.apps.count()}'
            )

            count += cat.apps.count()
        print(f'all apps: {count}\n\n')


class GameCategory(BaseCategory):
    CATEGORIES = [
        {'name_e': 'action games', 'name_f': 'اکشن'},
        {'name_e': 'arcade games', 'name_f': 'آرکید + تفننی'},
        {'name_e': 'strategy games', 'name_f': 'استراتژیک'},
        {'name_e': 'hd games', 'name_f': 'اچ دی'},
        {'name_e': 'without data games', 'name_f': 'بدون دیتا'},
        {'name_e': 'children games', 'name_f': 'کودکانه'},
        {'name_e': 'puzzle games', 'name_f': 'پازل و فکری'},
        {'name_e': 'simulation games', 'name_f': 'شبیه سازی'},
        {'name_e': 'card games', 'name_f': 'کارتی + تخته ای'},
        {'name_e': 'suggested games', 'name_f': 'بازیهای پیشنهادی'},
        {'name_e': 'racing', 'name_f': 'مسابقه ای'},
        {'name_e': 'musical games', 'name_f': 'موزیکال'},
        {'name_e': 'car and motor racing', 'name_f': 'موتور و ماشین سواری'},
        {'name_e': 'adventure', 'name_f': 'ماجراجویی'},
        {'name_e': 'role playing games', 'name_f': 'نقش آفرینی'},
        {'name_e': 'android game', 'name_f': 'بازی اندروید'},
        {'name_e': 'athletic', 'name_f': 'ورزشی'}
    ]

    @classmethod
    def show_information_category(cls):
        count = 0

        for category in cls.CATEGORIES:
            cat = cls.select().where(cls.name_e == category['name_e']).first()

            print(
                f'category: {cat.name_e.ljust(40)} \t\t'
                f'persian name: {cat.name_f.ljust(40)}\t\t'
                f'app count: {cat.games.count()}'
            )

            count += cat.games.count()
        print(f'all apps: {count}\n\n')
