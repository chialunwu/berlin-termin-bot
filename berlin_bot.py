import time
import os
import datetime
import os
import logging
import json
from platform import system
from playsound import playsound

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException

retry_seconds = 15

system = system()

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

def send_notification(title, message):
    script = 'display notification "{}" with title "{}"'.format(message, title)
    os.system('osascript -e \'{}\''.format(script))

class WebDriver:
    def __init__(self):
        self._driver: webdriver.Chrome
        self._implicit_wait_time = 20

    def __enter__(self) -> webdriver.Chrome:
        logging.info("Open browser")
        # some stuff that prevents us from being locked out
        options = webdriver.ChromeOptions() 
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')

        # Fallback: https://googlechromelabs.github.io/chrome-for-testing/#stable
        # self._driver = webdriver.Chrome('/Users/chialunwu/Downloads/chromedriver-mac-x64/chromedriver', options=options)
        self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self._driver.implicitly_wait(self._implicit_wait_time) # seconds
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        return self._driver

    def __exit__(self, exc_type, exc_value, exc_tb):
        logging.info("Close browser")
        self._driver.execute_script("window.onbeforeunload = null;")
        self._driver.quit()

class BerlinBot:
    def __init__(self, form, sound):
        self.form = form
        self.sound = sound

    def enter_start_page(self, driver: webdriver.Chrome):
        logging.info("Visit start page")
        driver.execute_script("window.onbeforeunload = null;")
        driver.execute_script("window.alert = function() {};")
        driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en")
        driver.find_element(By.XPATH, "//*[text()='Book Appointment']").click()
        time.sleep(5)

    def tick_off_some_bullshit(self, driver: webdriver.Chrome):
        logging.info("Ticking off agreement")
        driver.find_element(By.XPATH, "//*[contains(text(),'I hereby declare')]").click()
        for i in range(5):
            try:
                driver.find_element(By.ID, 'applicationForm:managedForm:proceed').click()
                break
            except:
                time.sleep(2)

    def enter_form(self, driver: webdriver.Chrome):
        logging.info("Fill out form")
        time.sleep(5)
        for i in range(10):
            try:
                s = Select(driver.find_element(By.ID, 'xi-sel-400'))
                s.select_by_visible_text(self.form["Citizenship"])
                break
            except:
                if i == 9:
                    raise e
                time.sleep(2)
        time.sleep(1)
        s = Select(driver.find_element(By.ID, 'xi-sel-400'))
        s.select_by_visible_text(self.form["Citizenship"])
        time.sleep(1)

        s = Select(driver.find_element(By.ID, 'xi-sel-422'))
        s.select_by_visible_text(self.form["Number of applicants"])
        time.sleep(1)

        with_family = self.form["Do you live in Berlin with a family member"]
        s = Select(driver.find_element(By.ID, 'xi-sel-427' ))
        s.select_by_visible_text(with_family)
        time.sleep(1)

        if with_family == "yes":
            s = Select(driver.find_element(By.ID, 'xi-sel-428' ))
            s.select_by_visible_text(self.form["Citizenship of the family member"])
            time.sleep(1)
        time.sleep(5)

        driver.find_element(By.XPATH, f"//*[contains(text(),'{self.form['Category']}')]").click()
        time.sleep(2)
        sub_category = self.form.get('Subcategory')
        if sub_category:
            driver.find_element(By.XPATH, f"//*[contains(text(),'{sub_category}')]").click()
            time.sleep(2)
        driver.find_element(By.XPATH, f"//*[contains(text(),'{self.form['Option']}')]").click()
        time.sleep(4)

        for _ in range(20):
            try:
                driver.find_element(By.ID, 'applicationForm:managedForm:proceed').click()
                break
            except:
                time.sleep(2)
        time.sleep(10)
    
    def _success(self, driver):
        logging.info("!!!SUCCESS - do not close the window!!!!")
        self.play_sound(self.sound['success'])
        send_notification("Termin!!!", "Hurry!!!")
        
        with open("success.txt", "a") as f:
            f.write(f"{datetime.datetime.now().isoformat()}\n")
        logging.info("Press Enter to start over")
        input()
        logging.info("Pray!")


    def run_once(self, driver):
        self.enter_start_page(driver)
        self.tick_off_some_bullshit(driver)
        self.enter_form(driver)

        # retry submit
        for i in range(500 // retry_seconds):
            for _ in range(3):
                active_tab = driver.find_element(By.CLASS_NAME, "antcl_active").text
                if active_tab:
                    break
                time.sleep(2)
            active_tab = active_tab.replace('\n', ' ')
            if active_tab and "Service selection" not in active_tab:
                self._success(driver)
                return True

            for j in range(3):
                try:
                    driver.find_element(By.ID, 'applicationForm:managedForm:proceed').click()
                    break
                except Exception as e:
                    if j == 2:
                        raise e
                    time.sleep(2)
            time.sleep(retry_seconds)
            logging.info(f"Retry - {i}")
        return False

    def run_loop(self):
        with WebDriver() as driver:
            bot.play_sound(self.sound['start'])
            while True:
                try:
                    success = self.run_once(driver)
                    if success:
                        return
                except Exception as e:
                    if 'Alert' in str(e):
                        raise e
                    self.play_sound(sound['error'])
                finally:
                    time.sleep(10)

    def play_sound(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        playsound(os.path.join(dir_path, filename))

if __name__ == "__main__":
    with open("form.json", "r") as f:
        form = json.load(f)
    with open("sound.json", "r") as f:
        sound = json.load(f)
    bot = BerlinBot(form, sound)
    while True:
        try:
            bot.run_loop()
        except Exception as e:
            print(e)
            bot.play_sound(sound['error'])
            time.sleep(10)

