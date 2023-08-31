import os,shutil, pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
load_dotenv()

class FBBot():
    
    def __init__(self):
        self.members_profile_link_li = []
        self.email_list = []
        self.group_link = ''
        self.facebook_process()
        self.main_df = pd.DataFrame(columns=['email', 'first_name'])
        self.Instagram()
        self.write_merged_csv()
        
    def Instagram(self):
        influence_df = pd.read_csv("influencer_details.csv")
        import pdb; pdb.set_trace()
        idf = influence_df[influence_df['check']==True]
        for user_link in idf['link'].tolist() : 
            print(user_link)
            user_link = str(user_link).split('/')
            
            user_link.reverse()
            
            for username in user_link :
                if username.strip():
                    self.get_all_insta_email(username)
        
    def get_all_insta_email(self, username):
        df = pd.read_csv(f'{username}.csv')
        df = df[pd.isna(df['email'])]
        df1 = pd.read_csv(f'{username}.csv')
        df2 = pd.read_csv('final_emails.csv')
        merged_df = pd.concat([df1, df2]).drop_duplicates(subset=['email'], keep='first')
        self.main_df = pd.concat([self.main_df, merged_df[['email', 'first_name']]])
        
    def write_merged_csv(self):
        self.main_df.to_csv('merged_unique_emails.csv', index=False)  # Write the accumulated data to a CSV file

    def get_driver(self):
        option = uc.ChromeOptions()
        user_dir = f'{os.getcwd()}/chrome_profile'
        option.add_argument(f'--user-data-dir={user_dir}')
        option.add_argument('--no-sandbox')
        option.add_argument(f'--profile=main')
        option.add_argument('--disable-popup-blocking')
        option.add_argument('--disable-notifications')
        option.add_argument('--disable-infobars')
        option.add_argument('--disable-extensions')
        option.add_argument('start-maximized')
        option.add_argument('--mute-audio')
        driver = uc.Chrome(options=option)
        driver.get('https://www.instagram.com/')
        self.driver = driver
        self.driver.maximize_window()
        self.driver.get('https://www.facebook.com/')
        
        return self.driver
        
        

    def delete_cache_folder(self,folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print("Cache folder deleted successfully.")
        else:
            print("Cache folder not found.")

        
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
                ele = wait_obj.until(EC.presence_of_element_located((locator_type, locator)))
                # ele = wait_obj.until( condition_func((locator_type, locator),*condition_other_args))
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

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=10, hide_keyboard=True):
        """Find an element, then input text and return it, or return None"""
        
        ele = self.find_element(element, locator, locator_type=locator_type,
                timeout=timeout)
        
        if ele:
            for i in range(3):
                try: 
                    ele.send_keys(text)
                    print(f'Inputed "{text}" for the element: {element}')
                    return ele    
                except ElementNotInteractableException :...
    
    def ScrollDown(self,px):
        self.driver.execute_script(f"window.scrollTo(0, {px})")
    
    def ensure_click(self, element):
        try:
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)
    
    def new_tab(self):
        self.driver.find_element(By.XPATH,'/html/body').send_keys(Keys.CONTROL+'t')

    def getvalue_byscript(self,script = '',reason=''):
        """made for return value from ele or return ele"""
        if reason :print(f'Script execute for : {reason}')
        else:
            print(f'execute_script : {script}')
        value = self.driver.execute_script(f'return {script}')  
        return value
        
    def CloseDriver(self):
        try: 
            self.driver.quit()
            print('Driver is closed !')
        except Exception as e: ...
        
    def get_group_id(self):
        group_df = pd.read_csv(f'{os.getcwd()}/fb_groups.csv')
        return group_df['group_links'].tolist()
        
    def facebook_process(self):
        self.get_driver()
        self.actions = ActionChains(self.driver)
        self.get_members()
        self.get_emails()
        df = pd.DataFrame(self.email_list)
        df.to_csv('final_emails.csv')
        
    def auto_login(self):
        if self.find_element('signup','/html/body/div[1]/div[1]/div/div/div[2]/div/div/span/a',By.XPATH,timeout=5) :
            self.input_text(os.getenv("NUMBER"),'phone numvber','/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div[1]/form/div/div[2]/input')
            self.input_text(os.getenv("PASSWORD"),'password','/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div[1]/form/div/div[4]/input')
            self.click_element('submit btn','/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div[1]/form/div/button')
    
    def get_new_members_list(self):
        before_member_profile_link_len = 0
        after_members_profile_link_len = 0
        self.auto_login()
        
        scroll = 2500
        self.ScrollDown(scroll)
        import time
        new_to_group = self.driver.find_elements(By.XPATH,'//div[contains(@class, "x1n2onr6 x1ja2u2z x9f619 x78zum5 xdt5ytf x2lah0s x193iq5w xx6bls6 x1jx94hy")]')[-1]
        self.actions.move_to_element(new_to_group).perform()
        try_no = 0
        
        while True :
            for _ in range(5):
                scroll += 5000
                self.ScrollDown(scroll)
                time.sleep(2)
                members_profile_link = self.driver.find_elements(By.XPATH,f'//a[contains(@class, "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")]')
                after_members_profile_link_len = len(members_profile_link)
                
                for i in range(before_member_profile_link_len,after_members_profile_link_len) :
                    member_link = ''
                    
                    member_link = members_profile_link[i]
                    if member_link :
                        member_link = member_link.get_attribute('href')
                        if 'user' in member_link.lower() :
                            if member_link not in self.members_profile_link_li :
                                self.members_profile_link_li.append(member_link.split('/user/')[-1].replace('/',''))
                                
                print(len(self.members_profile_link_li))
                
                scroll += 5000
                time.sleep(1)
                self.ScrollDown(scroll)
            if after_members_profile_link_len == before_member_profile_link_len : break
            before_member_profile_link_len = len(members_profile_link)
        
        
            
    def get_other_memeners_list(self,grp_link) :
        before_member_profile_link_len = 0
        after_members_profile_link_len = 0
        page_not_found = self.find_element('page not found','x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x1603h9y x1u7k74 x1xlr1w8 xi81zsa x2b8uid',By.CLASS_NAME,timeout=5)
        if page_not_found : return
        
        scroll = 2500
        self.ScrollDown(scroll)
        import time
        while True :
            
            for _ in range(3):
                scroll += 5000
                self.ScrollDown(scroll)
                time.sleep(2)
                members_profile_link = self.driver.find_elements(By.XPATH,f'//a[contains(@class, "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")]')
                if len(members_profile_link) > 2 and  len(self.members_profile_link_li) > 2:
                    after_index__ = 2
                else:
                    after_index__ = 0
                for member_link in members_profile_link[before_member_profile_link_len-after_index__:] :
                    members_profile_link.index(member_link)
                    if member_link :
                        
                        member_link = member_link.get_attribute('href')
                        print(member_link)
                        if 'user' in member_link.lower() :
                            member_link = member_link.split('/user/')[-1].replace('/','')
                            if member_link not in self.members_profile_link_li :
                                self.members_profile_link_li.append(member_link)
                                
                scroll += 5000
                time.sleep(1)
                self.ScrollDown(scroll)
                after_members_profile_link_len = len(self.members_profile_link_li)
            if after_members_profile_link_len == before_member_profile_link_len : 
                break
            before_member_profile_link_len = len(self.members_profile_link_li)

    def scrapp_email(self):
        links_elements = self.driver.find_elements(By.XPATH,'//span[contains(@class, "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")]')
            
        if links_elements != []:
            email = ''
            first_name_ = ''
            first_name =  self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1')
            for lk_ele in links_elements :
                email = lk_ele.text
                if first_name != [] :
                    first_name_ = first_name[0].text
                    
                if email :
                    if "@" in email.lower() and "." in email.lower() and first_name_ != '':
                        self.email_list.append({
                            "email" : email,
                            "firstname" :first_name_,
                            "group_link" :self.group_link
                        })
                        break
            else:
                self.email_list.append({
                        "email" : email,
                        "firstname" :first_name_,
                        "group_link" :self.group_link
                    })

    def get_email_from_page(self,first_name,id_):
        self.driver.get(f"https://www.facebook.com/search/pages/?q={first_name}")
        all_user_link_ele = self.driver.find_elements(By.XPATH,'//a[contains(@class, "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz xzsf02u x1rg5ohu")]')
        for user_link in all_user_link_ele :
            user_link = user_link.get_attribute('href')
            if user_link :
                if id_ in user_link.lower() :
                    self.driver.get(user_link)
                    self.scrapp_email()
        
        
    def get_emails(self):
        for user_prodile in self.members_profile_link_li:
            self.driver.get(f"https://www.facebook.com/profile.php?id={user_prodile}&sk=about_contact_and_basic_info")
            links_elements = self.driver.find_elements(By.XPATH,'//span[contains(@class, "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")]')
            
            if links_elements != []:
                for lk_ele in links_elements :
                    email = lk_ele.text
                    
                    first_name_ = ''
                    first_name =  self.driver.find_elements(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1')
                    if first_name != [] :
                        first_name_ = first_name[0].text
                        
                    if email :
                        if "@" in email.lower() and "." in email.lower() and first_name_ != '':
                            self.email_list.append({
                                "email" : email,
                                "firstname" :first_name_,
                                "group_link" :self.group_link
                            })
                            break
                else :
                    
                    self.get_email_from_page(first_name_,user_prodile)
    
    def get_members(self):
        member_types_li = [ "admins","experts","contributors","friends","things_in_common","near_you","members"]
        group_links = self.get_group_id()
        
        for grp_link in group_links :
            for member_type in member_types_li :
                
                if member_type == "members" :
                    self.driver.get(grp_link+'/'+member_type+'/')
                    self.get_new_members_list()
                    break
                else :
                    self.driver.get(grp_link+'/members'+'/'+member_type+'/')
                    self.get_other_memeners_list(grp_link)
            self.group_link = grp_link
            
            break
    
class ISTABot():
    def __init__(self):
        import subprocess
        subprocess.run(['python', 'get_follower.py'])
        subprocess.run(['python', 'get_details.py'])
    
ISTABot()
FBBot()