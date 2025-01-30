import os
import time
import random
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from src.persist import DataFramePersist

load_dotenv()


class WebScraper:
    def __init__(self, webdriver_url: str = None):
        self.webdriver_url = webdriver_url
        self.driver = self._init_driver()
        self.items = []
        self.urls = self._load_urls()
        self.persist = DataFramePersist(directory='data')

    def _init_driver(self):

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        options.add_argument(
            "accept-language=en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7")
        options.add_argument('cookie=indeed_rcc=CTK; CTK=1i5g84eusgb6388t; OptanonAlertBoxClosed=2024-09-06T11:12:53.910Z; FPID=FPID2.2.%2FWWKbBgUdZzBBDuvtu4bNRQjdwCoStAleG%2Bq2m3ZflU%3D.1723901035; _ga_5KTMMETCF4=GS1.1.1729003842.2.1.1729003961.42.0.0; CO=DE; LOCALE=de_DE; SESSION_START_TIME=1729631267314; SESSION_ID=1iar0tafi2g7k001; SESSION_END_TIME=1729631268892; _gcl_au=1.1.1552657794.1733411143; LC="co=DE & hl=de"; RF="O4UqZrkZHCPbiP8RwX6gJN1PYGeTmrV1BoP2WETzWGwwnNEzht5NVaVclH4MVP_BYXKc_w6hz8oMCXY1wMKexQ == "; _ga=GA1.1.501678285.1723901035; SURF=k8DCYzZEuq8PEQFGdjT2I434QDWsHbWz; SOCK="-IyUTKXcyxUnMZLv3SPtuDUoja4="; SHOE="G2b5caUSBE6VHCm-7MZtD8lrT4vBs9WsodJBJxDF1mCWZhFk4yO2eICo6xxzpNUYtMXvpnEVAIm9VPa28-6GASuxbMb8yS751brvvfzCyOTgDu_gIM5NHZFdLt7qTeFsx65-Y5Ce5y4Qs4uwc7csvTgE"; _cfuvid=1_p9kLO_Q4g149TrdPsFwHM39LN6vbYjatb9HPVbqfM-1737277531366-0.0.1.1-604800000; ENC_CSRF=qyQwbMKAqTh0Or8T1NUIzzyl65xbLnES; FPLC=lJ49vKMJr8mQC4T88P6b0PyL2gip2%2BMA%2BgigyyGW5WrOFnjA5dX%2BZ1Puu%2BwjZBc6LAJMONgGaCYgxeTEHxln%2FOM3iLNDZS6Dkgw8i8ZMrWXZ3k7XJrqzce7x9J87TA%3D%3D; CSRF=sJkZKtrXz9UQjl9X7grLPDrbCXjgJRU0; __cflb=02DiuGcjFCaWUgENVDZd4Hj4K3YwnMD4hwNroJNtdAEgL; MICRO_CONTENT_CSRF_TOKEN=dNfRBjt7ulzDU3TlzRV3uF4cHmuKrAfm; SHARED_INDEED_CSRF_TOKEN=GzJLrdLhNUQo8gVK5relbReFIaBkEYJY; INDEED_CSRF_TOKEN=doQLkbiKXWmNDfvfSqGGP0UCEWkDa7Dg; cf_clearance=3FFODALjLSPoaEz2vPbXzFpYsI3XaZOeTwuN96r2CoE-1737288614-1.2.1.1-c_nHchWHK7YbdgeLGCP0zDwilNs7DDxHCgAAuhtutZGZ0m9EL4Uvo3Ga3Jxiacqh.YNbEccFKbs17TRT86.LbKMddykJ2qeJeLK527olxz0GFPNhenOFuMntKuUOL7UewPwcbDg8UFWiDsh54rB8DVWS9reuYOhq3LdtAsKDY4.PPM9.BoMD9ASN3C9Y5S5EGcpHiMpygsAN6qDR03unohoDtqqNbyeLgoIk1Dwqg.EnPYa79QzLT7W.XYODFjw237jRI0ULALXAcRj742ROREc8oTvSMUaQuApeOfTg_BY; __cf_bm=Jo4hLuTJNN.RXpCCcdKU3mGLoiPQRQtn85SS9oOmR2M-1737290194-1.0.1.1-W1fbOGyJhXKNQ3lfpXVQE38wVl5fXcFl3p.4ZXhhiB6d0URGlSDao5ug3IBhzjIhCM_KmlJoHcFxOtaWKEmF0g; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jan+19+2025+13%3A44%3A06+GMT%2B0100+(Central+European+Standard+Time)&version=202409.2.0&isIABGlobal=false&hosts=&consentId=59175167-24b1-46c2-8c03-0102af2e86fa&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0007%3A1&geolocation=%3B&AwaitingReconsent=false&browserGpcFlag=0&isAnonUser=1; _ga_LYNT3BTHPG=GS1.1.1737290645.36.1.1737290647.0.0.1079188608')
        options.page_load_strategy = 'normal'
        return webdriver.Chrome(options=options)

    def _load_urls(self):
        items = []
        items = {
            'indeed': os.getenv("url_indeed"),
            'stepstone': os.getenv("url_stepstone"),
            'xing': os.getenv("url_xing"),
            # 'linkedin': os.getenv("url_linkedin"),
        }
        return items

    def anti_bot_behavior(self) -> None:
        ''' Anti-bot behavior to avoid detection '''
        try:
            self.driver.implicitly_wait(0.5)
            # Simulate human-like behavior
            time.sleep(random.uniform(1, 3))  # Random delay
            # move mouse
            ActionChains(self.driver).move_by_offset(
                10, 10).perform()  # Simulate mouse movement
            # scroll down
            self.driver.execute_script(
                # Scroll down
                "window.scrollTo(0, document.body.scrollHeight);")
            #
            time.sleep(random.uniform(1, 3))  # Random delay
        except Exception as e:
            print(f"error {e}")

    def fetch_page(self):
        ''' fetch all job titles from input websites '''
        try:
            for key, value in self.urls.items():
                print(f"Fetching page from {key} value {value}")
                #
                if key == 'stepstone':
                    self.fetch_page_stepstone_multipages(
                        key, value, max_pages=2)
                elif key == 'indeed':
                    self.fetch_page_indeed_multipages(key, value)
                elif key == 'xing':
                    self.fetch_page_xing_multipages(key, value)
                elif key == 'linkedin':
                    self.fetch_page_linkedin_multipages(key, value)
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

    def fetch_page_indeed(self, key: str, value: str, max_pages: int = 2):
        try:
            self.driver = self._init_driver()
            # test
            value = 'https://de.indeed.com/jobs?q=Data+Engineer&l=Deutschland'
            self.driver.get(value)

            # anti_bot_behavior
            self.anti_bot_behavior()

            #
            for page_number in range(max_pages):

                # get all job titles in current page
                elements = self.driver.find_elements(
                    By.XPATH, '//*[@class="css-1ac2h1w eu4oa1w0"]')

                for i in elements:
                    # click on item
                    try:
                        i.click()
                        # get job body
                        body_items = i.find_element(
                            By.XPATH, '//*[@id="jobDescriptionText"]')

                        # get every item as pretty text
                        item_text = i.get_attribute('innerText').strip()
                        item = {
                            'title': re.sub(r"[,:!-]", "", item_text),
                            'provider': key,
                            'provider_url': value,
                            'url': i.get_attribute('href'),
                            'body': re.sub(r"[,:!-]", "", body_items.get_attribute('innerText'))
                        }
                        self.items.append(item)
                        # Simulate human-like behavior
                        time.sleep(random.uniform(1, 3))  # Random delay
                        ActionChains(self.driver).move_by_offset(
                            10, 10).perform()  # Simulate mouse movement

                    except Exception as e:
                        print(e)
                        continue

                # go to next page
                # TODO: break if no next page exists
                xpath_next_page = f'//*[@data-testid="pagination-page-{
                    page_number+2}"]'
                next_page = self.driver.find_element(
                    By.XPATH, xpath_next_page)
                next_page.click()

            time.sleep(2)
            self.driver.quit()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()

    def fetch_page_indeed_multipages(self, key: str, value: str, max_pages: int = 2):
        ''' fetch indeed page with multiple pages '''
        try:
            self.driver = self._init_driver()
            # test
            value = 'https://de.indeed.com/jobs?q=Data+Engineer&l=Deutschland'
            self.driver.get(value)
            # anti_bot_behavior
            self.anti_bot_behavior()
            #
            for page_number in range(max_pages):
                # get all job titles in current page
                elements = self.driver.find_elements(
                    By.XPATH, '//*[@class="css-1ac2h1w eu4oa1w0"]')

                for i in elements:
                    # click on item
                    try:
                        # get every item as pretty text
                        item_text = i.get_attribute('innerText').strip()
                        item = {
                            'title': re.sub(r"[,:!-]", "", item_text),
                            'provider': key,
                            'provider_url': value,
                            'url': i.get_attribute('href'),
                            'body': ''
                        }
                        self.items.append(item)
                    except Exception as e:
                        print(e)
                        continue

                # go to next page
                # TODO: break if no next page exists
                xpath_next_page = f'//*[@data-testid="pagination-page-{
                    page_number+2}"]'
                next_page = self.driver.find_element(
                    By.XPATH, xpath_next_page)
                next_page.click()

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

            # anti_bot_behavior
            self.anti_bot_behavior()

            #
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

    def fetch_page_stepstone_multipages(self, key: str, value: str, max_pages: int = 2):
        try:
            self.driver = self._init_driver()
            self.driver.get(value)

            # anti_bot_behavior
            self.anti_bot_behavior()

            #
            for page_number in range(max_pages):
                # fetch page data
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

                # go to next page
                # TODO: break if no next page exists
                '''
                id 1 is the previous button
                '''
                xpath_next_page = f'//*[@aria-label="pagination"]/ul/li[{
                    page_number + 3}]/a'
                next_page = self.driver.find_element(
                    By.XPATH, xpath_next_page)
                next_page.click()

            time.sleep(2)
            self.driver.quit()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()

    def fetch_page_xing_multipages(self, key: str, value: str, max_pages: int = 2):
        ''' fetch xing page with multiple pages '''
        try:
            self.driver = self._init_driver()
            self.driver.get(value)

            # anti_bot_behavior
            self.anti_bot_behavior()

            #
            for page_number in range(max_pages):
                # fetch page data
                elements = self.driver.find_elements(
                    By.XPATH, '//li')

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

                # go to next page
                # TODO: break if no next page exists
                '''
                show more
                '''
                xpath_next_page = '//*[@id="app"]/div/div[2]/div/div[1]/div/main/div[2]/div[2]/button/div/span'
                next_page = self.driver.find_element(
                    By.XPATH, xpath_next_page)
                next_page.click()

            time.sleep(2)
            self.driver.quit()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()

    def fetch_page_linkedin_multipages(self, key: str, value: str, max_pages: int = 2):
        ''' fetch linkedin page with multiple pages '''
        try:
            self.driver = self._init_driver()
            self.driver.get(value)

            for page_number in range(max_pages):
                elements = self.driver.find_elements(
                    By.XPATH, '//*[contains(@class, "base-card__full-link")]')

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

                # go to next page
                # TODO: break if no next page exists
                xpath_next_page = f'//li[contains(@data-test-pagination-page-btn, "{
                    page_number + 2}")]'
                next_page = self.driver.find_element(
                    By.XPATH, xpath_next_page)
                next_page.click()

            time.sleep(2)
            self.driver.quit()
            return True
        except Exception as e:
            print(e)
            self.driver.quit()

    def close(self):
        self.driver.quit()
