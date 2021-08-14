import time

import pyshorteners.shorteners.chilpit
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager


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

        with Bar(message='Delay...', fill='@',
                 suffix='%(percent).1f%% - %(eta)ds', max=20, check_tty=False,
                 hide_cursor=False) as bar:
            for _ in range(20):
                time.sleep(1)
                bar.next()

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


if __name__ == '__main__':
    print(f"SteamUL Object\n{'-' * 80}")

    # SteamUnlocked object for user-inputted query
    query = SteamUL(input("Game:\t"))
    query.search_results()

    # Print names
    i = 1
    for item in query.results:
        print(f"[{i}] {query.results[item]['name']}")
        i += 1
    print('-' * 80)

    # Grab download link for the selected number
    print(query.download_link(int(input("Selection:\t"))))
