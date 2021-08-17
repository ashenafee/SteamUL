import os
import time

import pyshorteners.shorteners.chilpit
import requests
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from tqdm import trange
from webdriver_manager.chrome import ChromeDriverManager

os.environ['WDM_LOG_LEVEL'] = '0'


class SteamUL:
    """An object representing a SteamUnlocked query."""

    def __init__(self, query: str) -> None:
        """Initialize a new <SteamUL> object."""
        self.query = query
        self.search = f"https://steamunlocked.net/?s={self.query}"
        self.results = {}

    def search_results(self) -> None:
        """Grab the search results of <query> when searched on SteamUnlocked."""
        page = requests.get(self.search)
        soup = BeautifulSoup(page.content, "html.parser")

        # Find specific div containing search results
        page_results = soup.find('div', class_='col-lg-8 col-md-8 no-padding') \
            .find('div', class_='cover-items')

        # Populate dictionary with data on results
        for result in page_results.find_all('div'):
            item = {}
            try:
                title = result.find('div', class_='cover-item-title')
                image = result.find('div', class_='cover-item-image')

                # Create dictionary object based off the result's title
                name = title.text.strip()
                name = name[:name.index(' Free Download')]
                self.results[name] = item

                # Add link of result to its dictionary
                item['link'] = title.find('a').get('href')

                # Add image of result to its dictionary
                item['image'] = image.find('a').find('img').get('data-src')
            except AttributeError:
                pass

        # Sort dictionary off entry number
        keys = list(self.results.keys())

        for key in keys:
            previous = self.results[key]
            self.results.pop(key)
            self.results[keys.index(key) + 1] = previous
            self.results[keys.index(key) + 1]['name'] = key

    def download_link(self, choice: int) -> str:
        """Grab the download link for the selected result."""
        selected = self.results[choice]

        print(f"Grabbing download link for '{selected['name']}'...")

        # Grab page data for the selected game
        page = requests.get(selected['link'])
        soup = BeautifulSoup(page.content, "html.parser")

        # Specify ChromeOptions using seleniumwire
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Create Chrome webdriver
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        # Spoof the referer (make UploadHaven think you're coming directly from
        # SteamUnlocked).
        def interceptor(request):
            del request.headers['Referer']
            request.headers['Referer'] = 'https://steamunlocked.net/'

        driver.request_interceptor = interceptor

        # Load the UH page
        print(" ".join(soup.find('a', class_='btn-download').text.split()))
        driver.get(soup.find('a', class_='btn-download').get('href'))

        waiting_bar = trange(20, desc='Waiting', unit='s')
        for _ in waiting_bar:
            time.sleep(1)

        # Click button
        element = driver.find_element_by_xpath('//*[@id="submitFree"]')
        driver.execute_script("arguments[0].click();", element)

        # Get DDL
        ddl = driver.find_element_by_xpath('//*[@id="page-top"]/div/section'
                                           '/div/table/tbody/tr['
                                           '2]/td/div/div/a')

        # Shorten DDL using bit.ly
        s = pyshorteners.Shortener()
        short_ddl = s.chilpit.short(ddl.get_attribute('href'))
        driver.quit()

        # Save DDL to the game's dictionary
        selected['download'] = short_ddl

        return selected['download']

    def steam_info(self, choice) -> None:
        """Return the info on Steam's store for the selected game."""
        # Get Steam page for <game>
        s = requests.Session()
        response = s.get(f"https://store.steampowered.com/search/?term={self.results[choice]['name']}")
        soup = BeautifulSoup(response.content, "html.parser")
        page = soup.find('div', id='search_resultsRows').find('a').get('href')

        # Get info from <page>
        response = s.get(page)
        soup = BeautifulSoup(response.content, "html.parser")

        header_img = soup.find('img', class_='game_header_image_full').get('src')
        description = soup.find('div', class_='game_description_snippet').text.strip()
        all_reviews = soup.find_all('span', class_='nonresponsive_hidden responsive_reviewdesc')[1].text.strip()[2:]
        release = soup.find('div', class_='date').text.strip()
        developer = soup.find('div', id='developers_list').text.strip()
        publisher = soup.find_all('div', class_='dev_row')[1].find('div', class_='summary column').text.strip()
        # print(header_img)
        print("Steam link:\t" + response.url)
        print("Description:\t" + description)
        print("All reviews:\t" + all_reviews)
        print("Release date:\t" + release)
        print("Developer(s):\t" + developer)
        print("Publisher(s):\t" + publisher)


if __name__ == '__main__':
    pass
