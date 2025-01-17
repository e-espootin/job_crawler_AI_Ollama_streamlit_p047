from selenium import webdriver
# from selenium.webdriver import Remote, ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
from src.persist import DataFramePersist
import pandas as pd
load_dotenv()


SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

# TODO : go to next page
# TODO : click on job details
# TODO : get job details


class WebScraper:
    def __init__(self, webdriver_url: str = None):
        self.webdriver_url = webdriver_url
        self.driver = self._init_driver()
        self.items = []
        self.urls = self._load_urls()
        self.persist = DataFramePersist(directory='data')

    def _init_driver(self):
        # options = ChromeOptions()
        # options.add_argument("--headless")
        # return Remote(
        #     command_executor=self.webdriver_url,
        #     options=options,
        #     browser_profile=None,
        #     keep_alive=True,
        #     desired_capabilities=options.to_capabilities()
        # )
        return webdriver.Chrome()

    def _load_urls(self):
        items = []
        items = {
            'indeed': os.getenv("url_indeed"),
            'stepstone': os.getenv("url_stepstone")
        }
        return items

    def fetch_page(self):
        try:
            for key, value in self.urls.items():
                print(f"Fetching page from {key} value {value}")
                #
                if key == 'stepstone':
                    self.fetch_page_stepstone(key, value)
                elif key == 'indeed':
                    self.fetch_page_indeed(key, value)
                else:
                    print('not supported')
                # persist file into csv
                self.persist.save_dataframe(
                    pd.DataFrame(self.items), f"{key}.csv")

            #
            return True

        except Exception as e:
            print(e)
            self.driver.quit()

    def fetch_page_indeed(self, key: str, value: str):
        try:
            self.driver = self._init_driver()
            self.driver.get(value)
            elements = self.driver.find_elements(
                By.XPATH, '//*[@class="css-1ac2h1w eu4oa1w0"]')

            for i in elements:
                # get every item as pretty text
                item_text = i.get_attribute('innerText').strip()
                item = {
                    'title': item_text,
                    'provider': key,
                    'provider_url': value,
                    'url': i.get_attribute('href'),
                    'body': i.get_attribute('innerText')

                }
                self.items.append(item)

            time.sleep(2)
            self.driver.quit()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()

    def fetch_page_stepstone(self, key: str, value: str):
        try:
            self.driver = self._init_driver()
            self.driver.get(value)
            elements = self.driver.find_elements(
                By.XPATH, '//*[@class="res-1p8f8en"]')

            for i in elements:
                # get every item as pretty text
                item_text = i.get_attribute('innerText').strip()
                item = {
                    'title': item_text,
                    'provider': key,
                    'provider_url': value,
                    'url': i.get_attribute('href'),
                    'body': i.get_attribute('innerText')

                }
                self.items.append(item)

            time.sleep(2)
            self.driver.quit()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()

    def parse_page(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        return soup

    def close(self):
        self.driver.quit()

# Example usage:
# scraper = WebScraper(SBR_WEBDRIVER)
# page_source = scraper.fetch_page('http://example.com')
# soup = scraper.parse_page(page_source)
# scraper.close()
