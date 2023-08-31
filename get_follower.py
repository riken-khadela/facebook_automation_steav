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
    
def get_follower(driver,link):
    last = []
    driver.get(link)
    user = str(link).split('/')
    user = next(part for part in reversed(user) if part)
    follower_count_ele = find_element(driver,f'//*[@href="/{user}/followers/"]/span')
    if follower_count_ele:
        follower_count = follower_count_ele.get_attribute('title')
        if follower_count:
            driver.get(f'https://www.instagram.com/{user}/followers/')
            usernames = []
            while True:
                try:
                    existing_df = pd.read_csv(f'{user}.csv')
                except FileNotFoundError:
                    existing_df = pd.DataFrame()
                fBody  = find_element(driver,"//div[@class='_aano']")
                for i in range(10):
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
                a=find_elements(driver,'//*[@class="_aacl _aaco _aacw _aacx _aad7 _aade"]')
                last.append(len(a))
                new_usernames = [i.text for i in a if i.text not in existing_df['username'].values]
                if new_usernames:
                    breakpoint()
                    for username in new_usernames:
                        print(username)
                        if username not in existing_df['username'].values:
                            usernames.append(username)
                            username_links = f'https://www.instagram.com/{username}'
                            new_data = {'link': username_links, 'username': username,'first_name':'','time':'','bio':'','email':''}
                            new_df = pd.DataFrame([new_data])             
                            new_df.to_csv(f'{user}.csv', mode='a', index=False, header=False)
                if len(last) >= 10:
                    last_10_lengths = last[-20:]
                    if all(length == last_10_lengths[0] for length in last_10_lengths):
                        breakpoint()
                        break
            
            existing_df = pd.read_csv(f'{user}.csv')
            duplicates = existing_df['username'].duplicated(keep='first')
            existing_df = existing_df[~duplicates]
            existing_df.to_csv(f'{user}.csv', index=False)
            return usernames
    

def work(i):
    option = uc.ChromeOptions()
    user_dir = f'{os.getcwd()}/chrome_profile'
    option.add_argument(f'--user-data-dir={user_dir}')
    option.add_argument('--disable-popup-blocking')
    option.add_argument('--no-sandbox')
    option.add_argument(f'--profile=main')
    driver = uc.Chrome(options=option)
    driver.get('https://www.instagram.com/')
    submit = find_element(driver,'//button[@type="submit"]',timeout=5)
    if submit:
        print('please login, after login press C for continue')
        input("Please press enter when you are done with login process")
        with open('insta_cookies.pkl', 'rb') as file:cookies = pickle.load(file)
        for cookie in cookies:driver.add_cookie(cookie)
    df = pd.read_csv('influencer_details.csv')
    link = df.at[i,'link']
    driver.get(link)
    username = str(link).split('/')
    username = next(part for part in reversed(username) if part)
    print('scraping this user :',username)
    follower_count_ele = find_element(driver,f'//*[@href="/{username}/followers/"]/span')
    if follower_count_ele:
        follower_count = str(follower_count_ele.get_attribute('title')).replace(',','')
        if not df.at[i,'follower']:
            df.at[i,'follower'] = int(follower_count)
        df.to_csv('influencer_details.csv',index=False)
    try:
        df_1 = pd.read_csv(f'{username}.csv')
    except FileNotFoundError:
        df_1 = pd.DataFrame(columns=['link','username','first_name','time', 'bio' , 'email'])
        df_1.to_csv(f'{username}.csv',index=False)
    get_follower(driver,link)

        
    



df = pd.read_csv('influencer_details.csv')
for i in range(len(df)):
    if df.at[i,'check'] != True:
        work(i)
        df.at[i,'check'] = 'True'
        df.to_csv('influencer_details.csv',index=False)
