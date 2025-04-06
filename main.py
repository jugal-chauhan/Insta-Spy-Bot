#fill in your username and password 
username = 'schmxsby'
pw = 'Mozz@rell@Cheese511'

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
import numpy as np
from time import sleep
import time


class InstaBot:
    def __init__(self, username, pw):
        self.username = username
        self.pw = pw
        self.driver = None
        self.wait = None
        
        try:
            # Initialize Chrome with system ChromeDriver
            service = Service('/opt/homebrew/bin/chromedriver')
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1200,800')
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-popup-blocking')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Add user agent to look more like a real browser
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36')
            
            print("Initializing Chrome driver...")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Navigate to Instagram
            print("Navigating to Instagram...")
            self.driver.get("https://www.instagram.com")
            sleep(3)
            
            # Login
            print("Logging in...")
            
            # Wait for login form to be present
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form[method='post']"))
            )
            sleep(2)
            
            # Find and fill username field
            username_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
            )
            username_field.clear()
            sleep(1)
            for char in username:
                username_field.send_keys(char)
                sleep(0.1)  # Type like a human
            
            sleep(1)
            
            # Find and fill password field
            password_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            password_field.clear()
            sleep(1)
            for char in pw:
                password_field.send_keys(char)
                sleep(0.1)  # Type like a human
            
            sleep(1)
            
            # Find and click login button
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            login_button.click()
            sleep(5)
            
            # Handle "Save Login Info" popup if it appears
            try:
                save_info_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-"))
                )
                save_info_button.click()
                print("Clicked 'Not now' on save login info popup")
                sleep(2)
            except TimeoutException:
                print("No 'Save Login Info' popup appeared")
            
            # Handle "Turn on Notifications" popup if it appears
            try:
                notifications_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button._a9--._a9_1"))
                )
                notifications_button.click()
                print("Clicked 'Not Now' on notifications popup")
                sleep(2)
            except TimeoutException:
                print("No 'Turn on Notifications' popup appeared")
            
            # Verify login once after handling all popups
            self.verify_login()
            
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            self.close()
            raise

    def verify_login(self):
        """Verify we're still logged in, if not, relogin"""
        try:
            # Check if we're on the login page
            login_button = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
            if login_button:
                print("Redirected to login page. Attempting to relogin...")
                self.driver.get("https://www.instagram.com")
                sleep(3)
                
                # Try to login again
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "form[method='post']"))
                )
                sleep(2)
                
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
                )
                username_field.clear()
                sleep(1)
                for char in self.username:
                    username_field.send_keys(char)
                    sleep(0.1)
                
                sleep(1)
                
                password_field = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
                )
                password_field.clear()
                sleep(1)
                for char in self.pw:
                    password_field.send_keys(char)
                    sleep(0.1)
                
                sleep(1)
                
                login_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
                login_button.click()
                sleep(5)
            
            # Navigate to home page to verify login
            self.driver.get("https://www.instagram.com")
            sleep(3)
            
            # Check for various elements that indicate we're logged in
            try:
                # Try multiple selectors that indicate we're logged in
                selectors = [
                    "span[text()='Search']",
                    "a[href*='following']",
                    "a[href*='followers']",
                    "div[role='dialog']",
                    "button[aria-label='Close']",
                    "div[role='navigation']"
                ]
                
                for selector in selectors:
                    try:
                        self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        print("Login verified successfully")
                        return
                    except:
                        continue
                
                # If we get here, try one more time with a longer wait
                sleep(5)
                for selector in selectors:
                    try:
                        self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        print("Login verified successfully")
                        return
                    except:
                        continue
                
                raise Exception("Could not verify login with any known selectors")
                
            except Exception as e:
                print(f"Error verifying login: {str(e)}")
                raise Exception("Failed to verify login")
            
        except Exception as e:
            print(f"Error verifying login: {str(e)}")
            raise Exception("Failed to maintain login session")

    def _get_names(self, dialog):
        """Get all names from the dialog box"""
        names = []
        last_height = 0
        scroll_attempts = 0
        max_scroll_attempts = 30  # Maximum number of scroll attempts
        
        try:
            # Wait for the dialog content to load
            dialog_content = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
            )
            
            print("Scrolling to load all users...")
            while scroll_attempts < max_scroll_attempts:
                # Get all user items currently visible
                user_items = dialog_content.find_elements(
                    By.CSS_SELECTOR,
                    "div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1cy8zhl.x1oa3qoh.x1nhvcw1"
                )
                
                # Extract usernames from each user item
                for item in user_items:
                    try:
                        # Try to find username in the link
                        username_element = item.find_element(
                            By.CSS_SELECTOR,
                            "a[role='link'] span._ap3a._aaco._aacw._aacx._aad7._aade"
                        )
                        username = username_element.text
                        if username and username not in names:
                            names.append(username)
                            print(f"Found user: {username}")
                    except:
                        continue
                
                # Scroll the dialog
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", 
                    dialog_content
                )
                time.sleep(2)  # Wait for content to load
                
                # Get new height
                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight", 
                    dialog_content
                )
                
                # If height hasn't changed, we've either reached the bottom or content isn't loading
                if new_height == last_height:
                    scroll_attempts += 1
                    print(f"No new content loaded, attempt {scroll_attempts}/{max_scroll_attempts}")
                else:
                    scroll_attempts = 0  # Reset counter if we found new content
                    print(f"Found {len(names)} users so far...")
                
                last_height = new_height
                
                # If we've made multiple attempts and found no new content, we're probably at the bottom
                if scroll_attempts >= 3:
                    print("Reached the bottom of the list")
                    break
            
            print(f"Found a total of {len(names)} users")
            return names
            
        except Exception as e:
            print(f"Error getting names: {str(e)}")
            import traceback
            print("Full error:")
            print(traceback.format_exc())
            return []

    def get_unfollowers(self):
        """Get list of users who don't follow back"""
        try:
            # Verify login before proceeding
            self.verify_login()
            
            # Navigate to profile page
            print("Navigating to profile page...")
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(5)  # Wait longer for profile to load
            
            # Wait for profile page to load
            print("Waiting for profile page to load...")
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='following'], a[href*='followers']"))
            )
            time.sleep(2)
            
            # Get following list
            print("\nGetting following list...")
            following_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='following']"))
            )
            following_count = int(following_button.text.split()[0].replace(',', ''))
            print(f"You are following {following_count} users")
            
            # Try both normal click and JavaScript click
            try:
                following_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", following_button)
            time.sleep(3)
            
            # Get following list
            following_dialog = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
            )
            following = self._get_names(following_dialog)
            print(f"Successfully retrieved {len(following)} following")
            
            # Close following dialog
            print("Closing following dialog...")
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
            )
            try:
                close_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", close_button)
            time.sleep(3)
            
            # Make sure dialog is closed
            try:
                self.wait.until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
                )
            except:
                print("Warning: Following dialog might not be fully closed")
            
            # Get followers list
            print("\nGetting followers list...")
            followers_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='followers']"))
            )
            followers_count = int(followers_button.text.split()[0].replace(',', ''))
            print(f"You have {followers_count} followers")
            
            # Try both normal click and JavaScript click
            try:
                followers_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", followers_button)
            time.sleep(3)
            
            # Get followers list
            followers_dialog = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']"))
            )
            followers = self._get_names(followers_dialog)
            print(f"Successfully retrieved {len(followers)} followers")
            
            # Close followers dialog
            print("Closing followers dialog...")
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close']"))
            )
            try:
                close_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", close_button)
            time.sleep(3)
            
            # Calculate unfollowers
            unfollowers = [user for user in following if user not in followers]
            
            # Print results
            print("\nSummary:")
            print(f"Following: {len(following)} users")
            print(f"Followers: {len(followers)} users")
            print(f"Users who don't follow you back: {len(unfollowers)}")
            
            if unfollowers:
                print("\nUsers who don't follow you back:")
                for user in unfollowers:
                    print(f"- {user}")
            else:
                print("\nGreat! Everyone you follow also follows you back!")
            
            return unfollowers
            
        except Exception as e:
            print(f"\nError getting unfollowers: {str(e)}")
            import traceback
            print("\nFull error:")
            print(traceback.format_exc())
            return []

    def close(self):
        """Safely close the browser"""
        try:
            if self.driver:
                print("Closing browser...")
                try:
                    self.driver.quit()
                except WebDriverException:
                    print("Browser was already closed")
        except Exception as e:
            print(f"Error closing browser: {str(e)}")
        finally:
            self.driver = None
            self.wait = None

if __name__ == "__main__":
    my_bot = None
    try:
        my_bot = InstaBot(username, pw)
        my_bot.get_unfollowers()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if my_bot:
            my_bot.close()