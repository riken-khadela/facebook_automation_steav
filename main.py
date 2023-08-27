import os,shutil, pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class Bot():
    
    def __init__(self):
        self.members_profile_link_li = []
        self.facebook_process()

    
    
    def get_driver(self):
        option = uc.ChromeOptions()
        user_dir = f'{os.getcwd()}/chrome_profile'
        option.add_argument(f'--user-data-dir={user_dir}')
        option.add_argument('--disable-popup-blocking')
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
        # self.driver = webdriver.Chrome(executable_path='/media/rk/0E78-F7E7/facebook_automation/chromedriver',options=self.options)
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
        group_df = pd.read_csv('/home/rk/Desktop/facebook_automation/fb_groups.csv')
        return group_df['group_links'].tolist()
        ...
        
    
        
    def facebook_process(self):
        self.get_driver()
        self.actions = ActionChains(self.driver)
        self.driver.refresh()
        self.get_members()
        
        
    def auto_login(self):
        if self.find_element('signup','/html/body/div[1]/div[1]/div/div/div[2]/div/div/span/a',By.XPATH,timeout=5) :
            import pdb; pdb.set_trace()
            self.input_text('9978911838','phone numvber','/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div[1]/form/div/div[2]/input')
            self.input_text('Riken@112233','password','/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div[1]/form/div/div[4]/input')
            self.click_element('submit btn','/html/body/div[1]/div[1]/div/div/div[1]/div/div[2]/div/div[2]/div[1]/form/div/button')
            ...
    
    def get_new_members_list(self,grp_link):
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
                    # member_link = self.find_element('User link',f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[3]/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div[2]/div[19]/div/div[2]/div/div[7]/div/div/div[1]/span/span/a')
                    # member_link = self.find_element('User link',f'//a[contains(@class, "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")]')
                    
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
            if len(members_profile_link)> 1000 :break
            # ds = []
            # for ii in self.members_profile_link_li : ds.append({"group":grp_link.split('/groups/')[-1],"user" : ii.split('/user/')[-1].replace('/','')})
            # df = pd.DataFrame(ds)
            # df.to_csv('fb_groups_user.csv',index=False)
            
        
        import pdb; pdb.set_trace()
            
    def get_other_memeners_list(self,grp_link) :
        import pdb; pdb.set_trace()
        before_member_profile_link_len = 0
        after_members_profile_link_len = 0
        # self.auto_login()
        page_not_found = self.find_element('page not found','x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x1603h9y x1u7k74 x1xlr1w8 xi81zsa x2b8uid',By.CLASS_NAME)
        if page_not_found : return
        
        scroll = 2500
        self.ScrollDown(scroll)
        import time
        dd1 = 1
        while True :
            
            for _ in range(3):
                scroll += 5000
                self.ScrollDown(scroll)
                time.sleep(2)
                members_profile_link = self.driver.find_elements(By.XPATH,f'//a[contains(@class, "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")]')
                
                for member_link in members_profile_link :
                    if member_link :
                        if dd1 == 1 :
                            import pdb; pdb.set_trace()
                        
                        member_link = member_link.get_attribute('href')
                        print(member_link)
                        if 'user' in member_link.lower() :
                            member_link = member_link.split('/user/')[-1].replace('/','')
                            if member_link not in self.members_profile_link_li :
                                self.members_profile_link_li.append(member_link)
                                
                                
                print(len(self.members_profile_link_li))
                
                scroll += 5000
                time.sleep(1)
                self.ScrollDown(scroll)
                after_members_profile_link_len = len(self.members_profile_link_li)
            if after_members_profile_link_len == before_member_profile_link_len : break
            before_member_profile_link_len = len(self.members_profile_link_li)
    
    def get_emails(self):
        for user_prodile in self.members_profile_link_li:
            self.driver.get(f"https://www.facebook.com/profile.php?id={user_prodile}&sk=about_contact_and_basic_info")
            
            
            
            ...
    
    def get_members(self):
        member_types_li = [ "admins","experts","contributors","friends","things_in_common","near_you",]
        
        group_links = self.get_group_id()
        
        
        for grp_link in group_links :
            for member_type in member_types_li :
                self.driver.get(grp_link+'/members'+'/'+member_type+'/')
                
                if member_type == "members" :
                    self.get_new_members_list(grp_link)
                    break
                else :
                    self.get_other_memeners_list(grp_link)
            
        ...
        

Bot()