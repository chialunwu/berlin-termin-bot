import time
import platform
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
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


FORM_FILE = "/tmp/berlin_bot_form.json"

retry_seconds = 15

system = system()

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

def send_notification(title, message):
    if platform.system() == 'Darwin':
        try:
            script = 'display notification "{}" with title "{}"'.format(message, title)
            os.system('osascript -e \'{}\''.format(script))
        except Exception as e:
            logging.error(e)

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
        # self._driver = webdriver.Chrome('chromedriver absolute path', options=options)
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
        send_notification("!!Termin Found!!", "Hurry up!")
        
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
            self.play_sound(self.sound['start'])
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


class InputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.is_start = False

        try:
            with open(FORM_FILE, "r") as f:
                form = json.load(f)
        except:
            form = {}

        layout = QVBoxLayout()

        self.citizenship_label = QLabel("Citizenship (required):")
        self.citizenship_input = QLineEdit()
        self.citizenship_input.setText(form.get("Citizenship", ""))
        layout.addWidget(self.citizenship_label)
        layout.addWidget(self.citizenship_input)

        self.number_of_applicants_label = QLabel("Number of applicants (required):")
        self.number_of_applicants_input = QLineEdit()
        self.number_of_applicants_input.setText(form.get("Number of applicants", ""))
        layout.addWidget(self.number_of_applicants_label)
        layout.addWidget(self.number_of_applicants_input)

        self.with_family_label = QLabel("Do you live in Berlin with a family member (required):")
        self.with_family_input = QLineEdit()
        self.with_family_input.setText(form.get("Do you live in Berlin with a family member", ""))
        layout.addWidget(self.with_family_label)
        layout.addWidget(self.with_family_input)

        self.citizenship_of_the_family_member_label = QLabel("Citizenship of the family member:")
        self.citizenship_of_the_family_member_input = QLineEdit()
        self.citizenship_of_the_family_member_input.setText(form.get("Citizenship of the family member", ""))
        layout.addWidget(self.citizenship_of_the_family_member_label)
        layout.addWidget(self.citizenship_of_the_family_member_input)

        self.category_label = QLabel("Category (required):")
        self.category_input = QLineEdit()
        self.category_input.setText(form.get("Category", ""))
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)
        
        self.subcategory_label = QLabel("Subcategory:")
        self.subcategory_input = QLineEdit()
        self.subcategory_input.setText(form.get("Subcategory", ""))
        layout.addWidget(self.subcategory_label)
        layout.addWidget(self.subcategory_input)

        self.option_label = QLabel("Option (required):")
        self.option_input = QLineEdit()
        self.option_input.setText(form.get("Option", ""))
        layout.addWidget(self.option_label)
        layout.addWidget(self.option_input)

        self.start_button = QPushButton("Good luck")
        self.start_button.clicked.connect(self.start)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setWindowTitle("Your application")

    def start(self):
        cityzenship = self.citizenship_input.text()
        number_of_applicants = self.number_of_applicants_input.text()
        with_family = self.with_family_input.text()
        citizenship_of_the_family_member = self.citizenship_of_the_family_member_input.text()
        category = self.category_input.text()
        subcategory = self.subcategory_input.text()
        option = self.option_input.text()
    
        if not cityzenship or not number_of_applicants or not with_family or not category or not option:
            return
        
        form = {
            "Citizenship": cityzenship,
            "Number of applicants": number_of_applicants,
            "Do you live in Berlin with a family member": with_family,
            "Citizenship of the family member": citizenship_of_the_family_member,
            "Category": category,
            "Subcategory": subcategory,
            "Option": option,
        }
        with open(FORM_FILE, "w") as f:
            json.dump(form, f)
        self.is_start = True
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    input_form = InputForm()
    input_form.show()
    app.exec_()

    if input_form.is_start:
        with open(FORM_FILE, "r") as f:
            form = json.load(f)
        form = {k: v.strip() for k, v in form.items()}
        sound = {
            "start": "start.mp3",
            "success": "alarm.mp3",
            "error": "error.mp3"
        }
        bot = BerlinBot(form, sound)
        while True:
            try:
                bot.run_loop()
            except Exception as e:
                print(e)
                bot.play_sound(sound['error'])
                time.sleep(10)

