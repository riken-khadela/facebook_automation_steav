import time
import random
from glob import glob
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from selenium.common.exceptions import  WebDriverException
from requests.exceptions import RequestException
import requests,random, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import frame_to_be_available_and_switch_to_it




            
class Bot():
    def __init__(self) -> None:
        options = uc.ChromeOptions()
        # user_agents = [
        #     # Mobile user agents
        #     "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        #     "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
        #     # Desktop user agents
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        #     # Add more user agents here
        # ]
        # options.add_argument('--mute-audio')
        # options.add_argument('--disable-popup-blocking')
        # # options.add_argument('--no-sandbox')
        # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        # options.add_argument('--disable-gpu')
        options.add_argument(r'--user-data-dir=User Data')
        options.add_argument(r'--profile-directory=Profile')
        print(1111)
        import pdb; pdb.set_trace()
        # options.add_argument(f'user-agent={random.choice(user_agents)}')
        self.driver = uc.Chrome(user_data_dir='User Data')
    
    def find_element(self, element, locator, locator_type=By.XPATH,
            page=None, timeout=10,
            condition_func=EC.presence_of_element_located,
            condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.breakpoint()
        If it is more than zero, then wait for the element present.
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                #  ele = wait_obj.until(
                #          EC.presence_of_element_located(
                #              (locator_type, locator)))
                ele = wait_obj.until(
                        condition_func((locator_type, locator),
                            *condition_other_args))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.driver.find_element(by=locator_type,
                        value=locator)
            if page:
                print(
                        f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                print(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')
    
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)
        
        if ele:
            ele.click()
            print(f'Clicked the element: {element}')
            return ele
                

    def send_youtube_link(self): 
        # https://youtubeservices.com/free-youtube-views
        # https://www.instafollowers.co/free-youtube-views
        # https://www.instafollowers.co/free-instagram-views
        self.driver.get('https://www.instafollowers.co/free-youtube-views')
        input = self.find_element('input','//input[@class="form-control"]')
        input.send_keys('https://www.youtube.com/watch?v=Ui3wd6Tgrq0')
        get_view = self.find_element('get view','//*[@title="Get Free Views"]')
        time.sleep(2)
        if get_view:
            get_view.click()
        time.sleep(30)    
        while True:
            progress = self.find_element('progress','//*[@class="progress"]')
            if not progress:
                time.sleep(5)
                break
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
            verification = self.find_element('verification','//*[@class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox"]')  
            if verification:
                breakpoint()
        except NoSuchElementException:
            pass
        except Exception as e:print(e)
        
    def send_insta_link(self): 
        # https://youtubeservices.com/free-youtube-views
        # https://www.instafollowers.co/free-youtube-views
        # https://www.instafollowers.co/free-instagram-views
        self.driver.get('https://www.instafollowers.co/free-instagram-views')
        input = self.find_element('input','//input[@class="form-control"]')
        input.send_keys('https://www.youtube.com/watch?v=Ui3wd6Tgrq0')
        get_view = self.find_element('get view','//*[@title="Get Free Views"]')
        time.sleep(2)
        if get_view:
            get_view.click()
        time.sleep(30)    
        while True:
            progress = self.find_element('progress','//*[@class="progress"]')
            if not progress:
                time.sleep(5)
                break
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')))
            verification = self.find_element('verification','//*[@class="recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox"]')  
            if verification:
                breakpoint()
        except NoSuchElementException:
            pass
        except Exception as e:print(e)
        
    def send_yt_link(self):
        self.driver.get('https://youtubeservices.com/free-youtube-views')
        input = self.find_element('input','//input[@name="link"]')
        input.send_keys('https://www.youtube.com/watch?v=Ui3wd6Tgrq0')
        time.sleep(2)
        get_view = self.driver.find_elements(By.XPATH,'//button[@type="submit"]')
        time.sleep(2)
        if get_view:
            get_view[0].click()
        time.sleep(30)    
        while True:
            progress = self.find_element('progress','//*[@id="myProgress"]')
            if not progress:
                time.sleep(30)
                break
            error = self.find_element('error','//*[text()="You can use the free trial once a week. Please try again later."]')
            if error:
                break
        breakpoint()
        
        

bot = Bot()
bot.send_yt_link()