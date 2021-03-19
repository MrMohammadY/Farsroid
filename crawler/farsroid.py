import requests
from bs4 import BeautifulSoup
from ORM.model import AppsLinks, AppsData
from crawler.parser import Parser
from abc import ABC, abstractmethod
from threading import Thread
from queue import Queue


class BaseCrawler(ABC):

    @staticmethod
    def get(url):

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError or BaseException:
            return None

        if response.status_code == 200:
            return response

        return None

    @abstractmethod
    def run_crawler(self):
        pass


class FarsroidLinkCrawler(BaseCrawler):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def parser(response):
        list_links = list()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', attrs={'class': 'download-item'})
        for link in links:
            list_links.append(link['href'])

        return list_links

    def links_crawler(self, pages, index_thread):
        while pages.qsize():
            page = pages.get()

            response = self.get(self.url.format(page))

            if response is not None:

                links = self.parser(response)

                print(f'Thread: {index_thread}\t|\t'
                      f'Page: {page}\t|\t'
                      f'Capacity of crawled link: {len(links)}')

                AppsLinks.save_links(links)
                pages.task_done()
            else:
                pages.task_done()

    def run_crawler(self):
        threads = list()

        pages_queue = Queue()

        for page in range(1, 1300):
            pages_queue.put(page)

        for t in range(1, 21):
            thread = Thread(target=self.links_crawler, args=(pages_queue, t))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print('All Task Done...')


class FarsroidDataCrawler(BaseCrawler):
    def __init__(self):
        self.parser = Parser()
        self.links = self._set_links()

    @staticmethod
    def _set_links():
        return AppsLinks.load_links()

    def data_crawler(self, links, index_thread):
        while links.qsize():
            link = links.get()

            response = self.get(link)

            if response is not None:
                data = self.parser.parse(response, link)

                if data is not None:
                    app_data = data[0]
                    count = data[1]

                    print(
                        f'Thread: {index_thread}\t|\t'
                        f'Link: {link}\t|\t'
                        f'Count: {count}\t|\t'
                        f'Data crawled: {app_data}'
                    )
                    AppsData.save_app(app_data)
                    links.task_done()

                else:
                    links.task_done()
            else:
                links.task_done()

    def run_crawler(self):
        threads = list()

        links_queue = Queue()

        for link in self.links:
            links_queue.put(link.link)

        for t in range(1, 21):
            thread = Thread(target=self.data_crawler, args=(links_queue, t))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print('All Task Done...')
