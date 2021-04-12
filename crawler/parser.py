from bs4 import BeautifulSoup
import re


class Parser:
    def __init__(self):
        self.soup = None
        self.counter = 0

    @property
    def _set_name(self):
        try:
            name = self.soup.find('h1', attrs={'class': 'entry-title'})
            name = name.text.strip()
            name = name.replace('دانلود ', '')
            name = re.sub(r'–.*', '', name)
            return name
        except:
            return None

    @property
    def _set_image(self):
        try:
            image = self.soup.find('img', attrs={
                'class': 'attachment-217x217 size-217x217 wp-post-image lozad'})
            return image['data-src']
        except:
            return None

    @property
    def _set_download_links(self):
        list_links = list()
        try:
            links = self.soup.find_all('a', attrs={'class': 'download-btn'})

            for link in links:
                list_links.append(
                    {link.find('span').text.strip(): link['href']})

            return list_links
        except:
            return None

    @property
    def _set_information(self):
        list_information = list()
        try:
            information = self.soup.select('#downloadbox>div>table>tbody>tr>td')

            for i in information[:len(information) - 1]:
                list_information.append(i.text.strip())
            return list_information
        except:
            return None

    def parse(self, response, link, mode):
        self.soup = BeautifulSoup(response.content, 'html.parser')
        information = self._set_information

        if mode == 'app':
            if len(information) == 4:

                data = {
                    'name': self._set_name,
                    'image': self._set_image,
                    'download_links': self._set_download_links,
                    'last_updated': information[0],
                    'price': information[2],
                    'version': information[1],
                    'category': information[3],
                    'link': link
                }

                self.counter += 1

                if None not in data.values():
                    return data, self.counter

                return None
            return None

        elif mode == 'game':

            if len(information) == 6:

                data = {
                    'name': self._set_name,
                    'image': self._set_image,
                    'download_links': self._set_download_links,
                    'last_updated': information[0],
                    'price': information[3],
                    'version': information[1],
                    'age': information[2],
                    'internet': information[5],
                    'category': information[4],
                    'link': link
                }

                self.counter += 1

                if None not in data.values():
                    return data, self.counter

                return None
            return None
