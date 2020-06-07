#fill in your username and password 
username = ''
pw = ''

from selenium import webdriver
import numpy as np
from time import sleep


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://www.instagram.com")
        sleep(2)
        #self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        #sleep(2)
        login_field = self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        login_field = self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pw)
        login_field = self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)
        print("Number of people who do not follow us back : ")
        print(len(not_following_back))

    def _get_names(self):
        sleep(2)
        #sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        #sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

my_bot = InstaBot(username , pw)
my_bot.get_unfollowers()