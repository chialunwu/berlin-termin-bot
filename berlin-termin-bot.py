import sys
import termios
import tty
import select
import time
import platform
import os
import datetime
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
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCompleter
from PyQt5.QtCore import Qt


FORM_FILE = os.path.join(os.sep,'tmp', 'berlin_bot_form.json')
retry_seconds = 15
system = system()
FORM_OPTIONS = {
  "citizenship": [
    "Afghanistan",
    "African States, Other",
    "Albania",
    "Algeria",
    "American States, other",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Asian States, other",
    "Australia",
    "Australian States, other",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "British Overseas Territory in Africa",
    "British Overseas Territory in America",
    "British Overseas Territory in Asia",
    "British Overseas Territory in Australia",
    "British Overseas Territory in Europe",
    "Brunei Darussalam",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroons",
    "Canada",
    "Cape Verde",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo, Democratic Republic of",
    "Congo, Republic",
    "Cook Islands",
    "Costa Rica",
    "Côte d´Ivoire",
    "Cuba",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Eswatini",
    "Ethiopia",
    "European States, other",
    "Fiji",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Great Britain and Northern Ireland",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "India",
    "Indonesia",
    "Iran, Islamic Republic",
    "Iraq",
    "Israel",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Korea, Democratic People`s Republic ",
    "Korean Republic ",
    "Kosovo",
    "Krygyzstan",
    "Kuwait",
    "Laos, Democratic People`s Republic",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia, Federal States",
    "Moldavia, Republic of",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Niue",
    "Nortern Mariana Islands",
    "North Macedonia",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Qatar",
    "Russian Federation",
    "Rwanda",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "Southern Sudan",
    "Sri Lanka",
    "*stateless",
    "St. Kitts and Nevis",
    "St. Lucia",
    "St. Vincent and the Grenadines",
    "Sudan",
    "Suriname",
    "Switzerland",
    "Syria (family name A - E)",
    "Syria (family name F - Z)",
    "Taiwan",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United States of America",
    "*unresolved nationality (Palestinians and Kurds from Lebanon)",
    "*unresolved nationality / Palestinians from Syria (Family name  A – E)",
    "*unresolved nationality / Palestinians from Syria (Family name  F – Z)",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe"
  ],
  "numberOfPeople": [
    "one person",
    "two people",
    "three people",
    "four people",
    "five people",
    "six people",
    "seven people",
    "eight people"
  ],
  "liveWithFamily": ["yes", "no"],
  "category": [
    "Apply for a residence title",
    "Extend a residence title",
    "Transfer of a Residence title to a new passport",
    "Apply for a permanent settlement permit",
    "Passport substitute - Reissue",
    "Aufenthaltsgestattung (asylum procedure) - Extension",
    "Temporary suspension of deportation (Duldung) - Extension"
  ],
  "subcategory": [
    "Educational purposes",
    "Economic activity",
    "Family reasons",
    "Humanitarian grounds",
    "Special rights of residence"
  ],
  "option": [
    "Residence permit for attending a language course (sect. 16f para. 1)",
    "Residence permit for in-service training (sect. 16a)",
    "Residence permit for study preparation (sect. 16b para. 1)",
    "Residence permit for the purpose of studying (sect. 16b)",
    "Residence permit for the recognition of a foreign professional qualification in a non-regulated profession (§ 16d para. 3)",
    "Residence permit for the recognition of a foreign professional qualification in a non-regulated profession (sect. 16d para. 1)",
    "Residence permit for vocational training (sect. 16a)",
    "Residence permit to start a traineeship (sect. 19c para. 1)",
    "Residence permit to take part in a student exchange or to attend school (sect. 16f)",
    "Residence permit for a freelance employment - Issuance (sect. 21 para. 5)",
    "Residence permit for foreigners with a long-term residence in an EU member state (sect. 38a)",
    "Residence permit for job-seeking qualified skilled workers – Issuance (sect. 20)",
    "Residence permit for participation in a voluntary service (sect. 19c or 19e)",
    "Residence permit for qualified skilled workers with an academic education (sect. 18b)",
    "Residence permit for qualified skilled workers with vocational training (sect. 18a)",
    "Residence permit for scientific staff and research workers (sect. 18d)",
    "Residence permit for the purpose of self-employment - Issuance (sect. 21)",
    "Residence permit to start an employment as an Au-pair (sect. 19c para. 1)",
    "Residence permit for a newborn foreign child - Initial issuance (section 33)",
    "Residence permit for spouses and children of holders of an EU Blue Card (sect. 29-32)",
    "Residence permit for spouses and children of skilled workers, students, trainees, scientists and teachers (sect. 29-32)",
    "Residence permit for spouses, parents and children of foreign citizens (sect. 29-34)",
    "Residence permit for spouses, parents and children of German citizens (sect. 28)",
    "Residence permit for spouses, parents and children of persons eligible for subsidiary protection (sect. 36a)",
    "Residence card for family members of EU (except Germany) and EEA citizens",
    "Residence permit for freelancers and self-employed persons - Extension (sect. 21)",
    "Residence permit in cases of hardship - extension (sect. 23a)",
    "Residence permit issued on humanitarian grounds - Extension (sect. 22 - 25)",
    "Transfer of a Blue Card EU to a new passport",
    "Transfer of a permanent settlement permit or an EU long-term residence permit to a new passport",
    "Transfer of a residence card or permanent residence card to a new passport",
    "Transfer of a residence permit to a new passport",
    "Permanent residence card for family members of EU (except Germany) and EEA citizens",
    "Permanent settlement permit for children (sect. 35)",
    "Permanent settlement permit for family members of German citizens (sect. 28 para. 2)",
    "Travel document for foreigners (Reiseausweis) - Reissue",
    "Permission to reside (Aufenthaltsgestattung) - Extension",
    "Temporary suspension of deportation (Duldung) - Extension"
  ]
}
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

def clear_input_buffer():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            if select.select([sys.stdin], [], [], 0)[0]:
                sys.stdin.read(1)
            else:
                break
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

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
        logging.info("!!! SUCCESS - do not close the window !!!")
        self.play_sound(self.sound['success'])
        send_notification("!! Termin Found !!", "Hurry up!")
        logging.info("Press Enter to start over")
        clear_input_buffer()
        input()
        logging.info("Restarting...")


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
    def with_completer(self, qt_input):
        completer = QCompleter(qt_input.model(), self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        qt_input.setCompleter(completer)

    def __init__(self):
        super().__init__()
        self.is_start = False

        # Load form options data
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Load last configured form values
        try:
            with open(FORM_FILE, "r") as f:
                form = json.load(f)
        except:
            form = {}

        layout = QVBoxLayout()

        self.citizenship_label = QLabel("Citizenship (required):")
        self.citizenship_input = QComboBox(self)
        self.citizenship_input.setEditable(True)
        self.with_completer(self.citizenship_input)
        self.citizenship_input.addItems(FORM_OPTIONS.get("citizenship"))
        self.citizenship_input.setCurrentText(form.get("Citizenship", ""))
        layout.addWidget(self.citizenship_label)
        layout.addWidget(self.citizenship_input)

        self.number_of_applicants_label = QLabel("Number of applicants (required):")
        self.number_of_applicants_input = QComboBox(self)
        self.number_of_applicants_input.setEditable(True)
        self.with_completer(self.number_of_applicants_input)
        self.number_of_applicants_input.addItems(FORM_OPTIONS.get("numberOfPeople"))
        self.number_of_applicants_input.setCurrentText(form.get("Number of applicants", ""))
        layout.addWidget(self.number_of_applicants_label)
        layout.addWidget(self.number_of_applicants_input)

        self.with_family_label = QLabel("Do you live in Berlin with a family member (required):")
        self.with_family_input = QComboBox(self)
        self.with_family_input.setEditable(True)
        self.with_completer(self.with_family_input)
        self.with_family_input.addItems(FORM_OPTIONS.get("liveWithFamily"))
        self.with_family_input.setCurrentText(form.get("Do you live in Berlin with a family member", ""))
        layout.addWidget(self.with_family_label)
        layout.addWidget(self.with_family_input)

        self.citizenship_of_the_family_member_label = QLabel("Citizenship of the family member:")
        self.citizenship_of_the_family_member_input = QComboBox(self)
        self.citizenship_of_the_family_member_input.setEditable(True)
        self.with_completer(self.citizenship_of_the_family_member_input)
        self.citizenship_of_the_family_member_input.addItems(FORM_OPTIONS.get("citizenship"))
        self.citizenship_of_the_family_member_input.setCurrentText(form.get("Citizenship of the family member", ""))
        layout.addWidget(self.citizenship_of_the_family_member_label)
        layout.addWidget(self.citizenship_of_the_family_member_input)

        self.category_label = QLabel("Category (required):")
        self.category_input = QComboBox(self)
        self.category_input.setEditable(True)
        self.with_completer(self.category_input)
        self.category_input.addItems(FORM_OPTIONS.get("category"))
        self.category_input.setCurrentText(form.get("Category", ""))
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)
        
        self.subcategory_label = QLabel("Subcategory:")
        self.subcategory_input = QComboBox(self)
        self.subcategory_input.setEditable(True)
        self.with_completer(self.subcategory_input)
        self.subcategory_input.addItems(FORM_OPTIONS.get("subcategory"))
        self.subcategory_input.setCurrentText(form.get("Subcategory", ""))
        layout.addWidget(self.subcategory_label)
        layout.addWidget(self.subcategory_input)

        self.option_label = QLabel("Option (required):")
        self.option_input = QComboBox(self)
        self.option_input.setEditable(True)
        self.with_completer(self.option_input)
        self.option_input.addItems(FORM_OPTIONS.get("option"))
        self.option_input.setCurrentText(form.get("Option", ""))
        layout.addWidget(self.option_label)
        layout.addWidget(self.option_input)

        self.start_button = QPushButton("Good luck")
        self.start_button.clicked.connect(self.start)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setWindowTitle("Book LEA appointment")

    def start(self):
        cityzenship = self.citizenship_input.currentText()
        number_of_applicants = self.number_of_applicants_input.currentText()
        with_family = self.with_family_input.currentText()
        citizenship_of_the_family_member = self.citizenship_of_the_family_member_input.currentText()
        category = self.category_input.currentText()
        subcategory = self.subcategory_input.currentText()
        option = self.option_input.currentText()
    
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