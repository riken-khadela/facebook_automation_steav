import time, os, datetime,  pickle, re
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.service import Service
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor, wait
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


try:
    df = pd.read_csv('influencer_details.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['link','follower','check'])
    df.to_csv('influencer_details.csv', index=False)


def find_element(driver,xpath,locator=By.XPATH,timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        ele = wait.until(EC.presence_of_element_located((locator, xpath)))
        return ele
    except NoSuchElementException:
        pass
    except Exception as e:
        pass

def find_elements(driver, xpath, locator=By.XPATH, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        elements = wait.until(EC.presence_of_all_elements_located((locator, xpath)))
        return elements
    except NoSuchElementException:
        pass
    except Exception as e:
        pass

def click_popup(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoViewIfNeeded();", element)
    time.sleep(1)
    element.click()


option = webdriver.ChromeOptions()
user_dir = f'{os.getcwd()}/chrome_profile'
# option.add_argument(f'--user-data-dir={user_dir}')
option.add_argument('--disable-popup-blocking')
option.add_argument('--no-sandbox')
# option.add_argument(f'--profile=main')
# service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(options=option)
driver.get('https://www.instagram.com/')
submit = find_element(driver,'//button[@type="submit"]',timeout=5)
if submit:
    print('please login, after login press C for continue')
    with open('insta_cookies.pkl', 'rb') as file:cookies = pickle.load(file)
    for cookie in cookies:driver.add_cookie(cookie)
    
# for i in range(len(df)):
#     if df.at[i,'check'] == True:
#         username = str(df.at[i,'link']).split('/')
#         username = next(part for part in reversed(username) if part)
username = 'healthpreneur'
df_1 = pd.read_csv(f'{username}.csv')
for i in df_1.index:
    if  df_1.at[i,'check'] != True:
        driver.get(df_1.at[i, 'link'])
        
        first_name_ele = find_element(driver,'//*[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]',timeout=5)
        first_name = first_name_ele.text if first_name_ele else ""
        bio_ele = find_element(driver,'//*[@class="_aacl _aaco _aacu _aacx _aad6 _aade"]',timeout=2)
        bio = bio_ele.text.replace('\n', ' ') if bio_ele else ""
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', bio)
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', bio)
        emails_str = ', '.join(emails) if emails else ''
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_1.at[i,'first_name'] = first_name
        df_1.at[i,'time'] = now_time
        df_1.at[i,'bio'] = bio
        df_1.at[i,'email'] = emails_str
        df_1.at[i,'check'] = 'True'
        df_1.to_csv(f'{username}.csv', index=False)
driver.quit()