from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def test_chrome_setup():
    try:
        print("Initializing Chrome WebDriver...")
        service = Service('/opt/homebrew/bin/chromedriver')
        driver = webdriver.Chrome(service=service)
        print("Chrome WebDriver initialized successfully!")
        
        print("Opening Google to test...")
        driver.get("https://www.google.com")
        print("Test completed successfully!")
        
        driver.quit()
        print("Chrome WebDriver closed successfully!")
        return True
    except Exception as e:
        print("An error occurred: {}".format(str(e)))
        return False

if __name__ == "__main__":
    test_chrome_setup() 