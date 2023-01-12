import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
DEFAULT_CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'


class PaywallHandler:
    def __init__(self, virtualizeDisplay) -> None:
        self.domain = 'https://archive.ph/'

        # Only used for Pi/headless devices
        if virtualizeDisplay:
            currentdisplay = Display(visible=0, size=(800, 600))
            currentdisplay.start()
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            # This is a bit hacky, but needed for headless browsers https://stackoverflow.com/questions/56436173/python-selenium-chromedriver-not-working-with-headless-option
            chrome_options.add_argument(f'user-agent={DEFAULT_USER_AGENT}')
            self.driver = webdriver.Chrome(DEFAULT_CHROMEDRIVER_PATH, options=chrome_options)
        else:
            self.driver = webdriver.Chrome()

        self.__init_submission()

    # Internal function to init all the required components.
    def __init_submission(self):
        self.driver.get(self.domain)
        assert 'Webpage archive' in self.driver.title
        elem = self.driver.find_element(By.ID, 'url')
        elem.clear()

    # Internal function to request archived/processed URL
    def __request_url(self, url):
        # Make sure we're still where we want to be. Will throw exception if not
        assert 'Webpage archive' in self.driver.title
        elem = self.driver.find_element(By.ID, 'url')
        elem.clear()
        elem.send_keys(url)
        elem.send_keys(Keys.RETURN)

    # External Function to handle URL Submission.
    def submit_url(self, url):
        logging.info(f'Requesting URL: {url}')
        self.__request_url(url)

        if '/wip/' in self.driver.current_url:
            logging.debug(f'WIP result detected. URL: {url}')
            raise WorkInProgressException(self.driver.current_url)

        logging.info(f'Result: {self.driver.current_url}')
        return self.driver.current_url


# Custom Exception used to communicate WIP status
class WorkInProgressException(Exception):
    def __init__(self, url, *args: object) -> None:
        self.currentURL = url
        super().__init__(*args)
