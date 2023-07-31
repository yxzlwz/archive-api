import base64
import re
import time

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from .optimize_config import optimize_config

WIDTH = 1920
HEIGHT = 1080


class SeleniumChrome:

    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        )
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches',
                                        ['enable-outomation'])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(WIDTH, HEIGHT)
        driver.implicitly_wait(10)
        self.driver = driver

    def archive(self, url, filename, config):
        start_time = time.time()
        self.driver.get(url)
        if config['lazyload']:
            self.lazy_load()
        if config['optimize']:
            self.optimize()
        title = self.get_title()
        images = self.save_as_images(filename)
        pdfs = self.save_as_pdfs(filename)
        return {
            'title': title,
            'images': images,
            'pdfs': pdfs,
        }, {
            'engine': 'selenium_chrome',
            'proxy': None,
            'genuine_url': self.driver.current_url,
            'time': round(time.time() - start_time, 2),
        }

    def lazy_load(self):
        height = self.driver.execute_script(
            'return document.body.parentNode.scrollHeight')
        _height = 0
        while _height < height:
            _height += HEIGHT // 2
            self.driver.execute_script(f'window.scrollTo(0, {_height});')
            time.sleep(0.5)
        self.driver.execute_script('window.scrollTo(0, 0);')

    def optimize(self):
        domain = self.driver.execute_script('return document.domain')
        if domain not in optimize_config:
            return
        path = self.driver.execute_script('return document.location.pathname')
        for pattern, config in optimize_config[domain].items():
            if not re.match(pattern, path):
                continue
            if config['action'] == 'click':
                self.driver.find_element(
                    by=By.CSS_SELECTOR,
                    value=config['element'],
                ).click()
            elif config['action'] == 'wait':
                time.sleep(config['seconds'])

    def get_title(self):
        return self.driver.title or self.driver.current_url

    def save_as_images(self, filename):
        _height = self.driver.execute_script(
            'return document.body.scrollHeight')
        if _height == 0:
            return []
        height = self.driver.execute_script(
            'return document.body.parentNode.scrollHeight')
        self.driver.set_window_size(WIDTH, max(height, HEIGHT))
        body = self.driver.find_element(by=By.TAG_NAME, value='body')
        body.screenshot(
            str(settings.ARCHIVE_FILE_PATH / f'images/{filename}.png'))
        return [f'{settings.ARCHIVE_FILE_URL_PREFIX}/images/{filename}.png']

    def save_as_pdfs(self, filename):
        pdf = self.driver.execute_cdp_cmd('Page.printToPDF',
                                          {'printBackground': True})
        (settings.ARCHIVE_FILE_PATH / f'pdfs/{filename}.pdf').write_bytes(
            base64.b64decode(pdf['data']))
        return [f'{settings.ARCHIVE_FILE_URL_PREFIX}/pdfs/{filename}.pdf']
