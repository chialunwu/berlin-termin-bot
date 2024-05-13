import sys
# import termios
import msvcrt
# import tty
# import select
import time
import platform
import os
import logging
import json
import threading
import queue

from platform import system
from playsound import playsound

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QCompleter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


SOUND = {
    "start": "start.mp3",
    "success": "alarm.mp3",
    "error": "error.mp3"
}
system = system()
IMMIGRATION_FORM_OPTIONS = {
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
            script = 'display notification "{}" with title "{}"'.format(
                message, title)
            os.system('osascript -e \'{}\''.format(script))
        except Exception as e:
            logging.error(e)


def clear_input_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()


def get_input(q):
    try:
        user_input = input()
        q.put(user_input)
    except EOFError:
        q.put(None)


def input_with_timeout(prompt, timeout):
    clear_input_buffer()
    q = queue.Queue()
    thread = threading.Thread(target=get_input, args=(q,))
    thread.start()
    try:
        logging.info(prompt)
        user_input = q.get(timeout=timeout)
    except queue.Empty:
        logging.warning("Input timeout reached. Continuing with program...")
        user_input = None
    thread.join(timeout=0.1)
    return user_input


def load_form(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return {}


def update_form(filepath, form):
    with open(filepath, "w") as f:
        json.dump(form, f)


class WebDriver:
    def __init__(self):
        self._driver: webdriver.Chrome
        self._implicit_wait_time = 20

    def __enter__(self) -> webdriver.Chrome:
        logging.info("Open browser")
        # some stuff that prevents us from being locked out
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2})
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')

        # Fallback: https://googlechromelabs.github.io/chrome-for-testing/#stable
        # self._driver = webdriver.Chrome('chromedriver absolute path', options=options)
        self._driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        self._driver.implicitly_wait(self._implicit_wait_time)  # seconds
        self._driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                                     "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        return self._driver

    def __exit__(self, exc_type, exc_value, exc_tb):
        logging.info("Close browser")
        self._driver.execute_script("window.onbeforeunload = null;")
        self._driver.quit()


class BerlinImmigrationOfficeBot:
    def __init__(self, form):
        self.form = form
        self.retry_seconds = 15
        self.attempts = 0

    def enter_start_page(self, driver: webdriver.Chrome):
        logging.info("Visiting start page")
        driver.execute_script("window.onbeforeunload = null;")
        driver.execute_script("window.alert = function() {};")
        driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en")
        driver.find_element(By.XPATH, "//*[text()='Book Appointment']").click()
        time.sleep(5)

    def tick_off_agreement(self, driver: webdriver.Chrome):
        logging.info("Ticking off agreement")
        driver.find_element(
            By.XPATH, "//*[contains(text(),'I hereby declare')]").click()
        for i in range(5):
            try:
                driver.find_element(
                    By.ID, 'applicationForm:managedForm:proceed').click()
                break
            except:
                time.sleep(2)

    def enter_form(self, driver: webdriver.Chrome):
        logging.info("Filling out form")
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
        s = Select(driver.find_element(By.ID, 'xi-sel-427'))
        s.select_by_visible_text(with_family)
        time.sleep(1)

        if with_family == "yes":
            s = Select(driver.find_element(By.ID, 'xi-sel-428'))
            s.select_by_visible_text(
                self.form["Citizenship of the family member"])
            time.sleep(1)
        time.sleep(5)

        driver.find_element(
            By.XPATH, f"//*[contains(text(),'{self.form['Category']}')]").click()
        time.sleep(2)
        sub_category = self.form.get('Subcategory')
        if sub_category:
            driver.find_element(
                By.XPATH, f"//*[contains(text(),'{sub_category}')]").click()
            time.sleep(2)
        driver.find_element(
            By.XPATH, f"//*[contains(text(),'{self.form['Option']}')]").click()
        time.sleep(4)

        for _ in range(20):
            try:
                driver.find_element(
                    By.ID, 'applicationForm:managedForm:proceed').click()
                break
            except:
                time.sleep(2)
        time.sleep(10)

    def _success(self):
        logging.info("!!! SUCCESS - do not close the window !!!")
        self.play_sound(SOUND['success'])
        send_notification("!! Immigration Office Termin Found !!", "Hurry up!")
        input_with_timeout("Press Enter to start over (5 minute timeout)", 300)
        logging.info("Restarting...")

    def run_once(self, driver):
        self.enter_start_page(driver)
        self.tick_off_agreement(driver)
        self.enter_form(driver)

        for _ in range(500 // self.retry_seconds):
            logging.info(
                f"Attempt: {self.attempts} (retry in {self.retry_seconds} seconds)")
            self.attempts += 1
            for _ in range(3):
                active_tab = driver.find_element(
                    By.CLASS_NAME, "antcl_active").text
                if active_tab:
                    break
                time.sleep(2)
            active_tab = active_tab.replace('\n', ' ')
            if active_tab and "Service selection" not in active_tab:
                self._success(driver)
                return True

            for j in range(3):
                try:
                    driver.find_element(
                        By.ID, 'applicationForm:managedForm:proceed').click()
                    break
                except Exception as e:
                    if j == 2:
                        raise e
                    time.sleep(2)
            time.sleep(self.retry_seconds)
        return False

    def run_loop(self):
        with WebDriver() as driver:
            self.play_sound(SOUND['start'])
            while True:
                try:
                    success = self.run_once(driver)
                    if success:
                        return
                except Exception as e:
                    if 'Alert' in str(e):
                        raise e
                    self.play_sound(SOUND['error'])
                finally:
                    time.sleep(10)

    def play_sound(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        playsound(os.path.join(dir_path, filename))


class BerlinCitizenOfficeBot:
    def __init__(self, url):
        self.retry_seconds = 50
        self.url = url

    def enter_start_page(self, driver: webdriver.Chrome):
        driver.execute_script("window.onbeforeunload = null;")
        driver.execute_script("window.alert = function() {};")
        driver.get(self.url)
        driver.implicitly_wait(10)

    def _success(self):
        logging.info("!!! SUCCESS - do not close the window !!!")
        self.play_sound(SOUND['success'])
        send_notification("!! Bürgeramt Termin Found !!", "Hurry up!")
        input_with_timeout("Press Enter to start over (5 minute timeout)", 300)
        logging.info("Restarting...")

    def run_once(self, driver):
        self.enter_start_page(driver)
        try:

            element = driver.find_element(
                By.XPATH, f"//*[contains(text(),'Bitte wählen Sie ein Datum')]")
            if element:
                self._success()
                return True
        except:
            pass

    def run_loop(self):
        with WebDriver() as driver:
            self.play_sound(SOUND['start'])
            logging.info(
                f"Checking {self.url} every 60 seconds (checking more frequently could get you blocked for 1 hour)")
            attempts = 0
            while True:
                try:
                    logging.info(f"Attempt: {attempts} (retry in 60 seconds)")
                    success = self.run_once(driver)
                    if not success:
                        time.sleep(self.retry_seconds)
                except Exception as e:
                    self.play_sound(SOUND['error'])
                    time.sleep(10)
                finally:
                    attempts += 1

    def play_sound(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        playsound(os.path.join(dir_path, filename))


class LEAInputForm(QWidget):
    # FORM_FILE = os.path.join(os.sep, 'tmp', 'berlin_bot_form.json')
    FORM_FILE = os.path.join(os.path.dirname(__file__), 'berlin_bot_form.json')

    def with_completer(self, qt_input):
        completer = QCompleter(qt_input.model(), self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.popup().setFont(qt_input.font())
        qt_input.setCompleter(completer)

    def __init__(self):
        super().__init__()

        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        self.form = None

        self.form = load_form(LEAInputForm.FORM_FILE)

        layout = QVBoxLayout()

        self.citizenship_label = QLabel("Citizenship (required):")
        self.citizenship_input = QComboBox(self)
        self.citizenship_input.setEditable(True)
        self.with_completer(self.citizenship_input)
        self.citizenship_input.addItems(
            IMMIGRATION_FORM_OPTIONS.get("citizenship"))
        self.citizenship_input.setCurrentText(self.form.get("Citizenship", ""))
        layout.addWidget(self.citizenship_label)
        layout.addWidget(self.citizenship_input)

        self.number_of_applicants_label = QLabel(
            "Number of applicants (required):")
        self.number_of_applicants_input = QComboBox(self)
        self.number_of_applicants_input.setEditable(True)
        self.with_completer(self.number_of_applicants_input)
        self.number_of_applicants_input.addItems(
            IMMIGRATION_FORM_OPTIONS.get("numberOfPeople"))
        self.number_of_applicants_input.setCurrentText(
            self.form.get("Number of applicants", ""))
        layout.addWidget(self.number_of_applicants_label)
        layout.addWidget(self.number_of_applicants_input)

        self.with_family_label = QLabel(
            "Do you live in Berlin with a family member (required):")
        self.with_family_input = QComboBox(self)
        self.with_family_input.setEditable(True)
        self.with_completer(self.with_family_input)
        self.with_family_input.addItems(
            IMMIGRATION_FORM_OPTIONS.get("liveWithFamily"))
        self.with_family_input.setCurrentText(self.form.get(
            "Do you live in Berlin with a family member", ""))
        layout.addWidget(self.with_family_label)
        layout.addWidget(self.with_family_input)

        self.citizenship_of_the_family_member_label = QLabel(
            "Citizenship of the family member (optional):")
        self.citizenship_of_the_family_member_input = QComboBox(self)
        self.citizenship_of_the_family_member_input.setEditable(True)
        self.with_completer(self.citizenship_of_the_family_member_input)
        self.citizenship_of_the_family_member_input.addItems(
            IMMIGRATION_FORM_OPTIONS.get("citizenship"))
        self.citizenship_of_the_family_member_input.setCurrentText(
            self.form.get("Citizenship of the family member", ""))
        layout.addWidget(self.citizenship_of_the_family_member_label)
        layout.addWidget(self.citizenship_of_the_family_member_input)

        self.category_label = QLabel("Category (required):")
        self.category_input = QComboBox(self)
        self.category_input.setEditable(True)
        self.with_completer(self.category_input)
        self.category_input.addItems(IMMIGRATION_FORM_OPTIONS.get("category"))
        self.category_input.setCurrentText(self.form.get("Category", ""))
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)

        self.subcategory_label = QLabel("Subcategory (optional):")
        self.subcategory_input = QComboBox(self)
        self.subcategory_input.setEditable(True)
        self.with_completer(self.subcategory_input)
        self.subcategory_input.addItems(
            IMMIGRATION_FORM_OPTIONS.get("subcategory"))
        self.subcategory_input.setCurrentText(self.form.get("Subcategory", ""))
        layout.addWidget(self.subcategory_label)
        layout.addWidget(self.subcategory_input)

        self.option_label = QLabel("Option (required):")
        self.option_input = QComboBox(self)
        self.option_input.setEditable(True)
        self.with_completer(self.option_input)
        self.option_input.addItems(IMMIGRATION_FORM_OPTIONS.get("option"))
        self.option_input.setCurrentText(self.form.get("Option", ""))
        layout.addWidget(self.option_label)
        layout.addWidget(self.option_input)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)
        self.start_button.setFixedHeight(40)
        layout.addSpacing(20)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

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

        self.form = {
            "Citizenship": cityzenship,
            "Number of applicants": number_of_applicants,
            "Do you live in Berlin with a family member": with_family,
            "Citizenship of the family member": citizenship_of_the_family_member,
            "Category": category,
            "Subcategory": subcategory,
            "Option": option,
        }
        update_form(LEAInputForm.FORM_FILE, self.form)


class OtherInputForm(QWidget):
    FORM_FILE = os.path.join(os.sep, 'tmp', 'other_form.json')

    def __init__(self):
        super().__init__()

        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

        form = load_form(OtherInputForm.FORM_FILE)
        self.url = None

        layout = QVBoxLayout()
        self.url_label = QLabel(f"Service URL (required):\n\n" +
                                "For example, for the service - https://service.berlin.de/dienstleistung/120686/,\nright click the 'Berlinweite Terminbuchung' button and click 'Copy Link Address'")
        self.url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.url_input = QComboBox(self)
        self.url_input.setEditable(True)
        self.url_input.setCurrentText(form.get("url", ""))
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)
        self.start_button.setFixedHeight(40)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start(self):
        self.url = self.url_input.currentText()
        if not self.url:
            return
        update_form(OtherInputForm.FORM_FILE, {"url": self.url})


class EntryForm(QWidget):
    def __init__(self):
        super().__init__()

        font = QFont()
        font.setPointSize(18)
        self.button_immigration = QPushButton("Immigration Office 🛂", self)
        self.button_immigration.setFixedHeight(40)
        self.button_immigration.setFont(font)
        self.button_anmeldung = QPushButton("Anmeldung einer Wohnung 🏠", self)
        self.button_anmeldung.setFixedHeight(40)
        self.button_anmeldung.setFont(font)
        self.button_other = QPushButton("Other Bürgeramt services", self)
        self.button_other.setFixedHeight(40)
        self.button_other.setFont(font)

        self.form_immigration = LEAInputForm()
        self.form_immigration.setVisible(False)
        self.form_other = OtherInputForm()
        self.form_other.setVisible(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button_immigration)
        layout.addSpacing(20)
        layout.addWidget(self.button_anmeldung)
        layout.addWidget(self.form_immigration)
        layout.addWidget(self.form_other)
        layout.addSpacing(20)
        layout.addWidget(self.button_other)
        self.setLayout(layout)

        self.button_immigration.clicked.connect(self.show_form_immigration)
        self.button_anmeldung.clicked.connect(self.start_anmeldung)
        self.button_other.clicked.connect(self.show_form_other)
        self.immigration_form = None
        self.citizen_service_url = None

        self.setContentsMargins(70, 70, 70, 70)
        self.setWindowTitle("Berlin Termin Bot")

    def hide_buttons(self):
        self.button_immigration.setVisible(False)
        self.button_anmeldung.setVisible(False)
        self.button_other.setVisible(False)

    def show_form_immigration(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.form_immigration.setVisible(True)
        self.form_immigration.start_button.clicked.connect(
            self.start_immigration)
        self.hide_buttons()

    def show_form_other(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.form_other.setVisible(True)
        self.form_other.start_button.clicked.connect(self.start_other)
        self.hide_buttons()

    def start_immigration(self):
        if self.form_immigration.form:
            self.immigration_form = self.form_immigration.form
            self.close()

    def start_anmeldung(self):
        self.citizen_service_url = "https://service.berlin.de/terminvereinbarung/termin/all/120686/"
        self.close()

    def start_other(self):
        if self.form_other.url:
            self.citizen_service_url = self.form_other.url
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    entry_form = EntryForm()
    entry_form.show()
    app.exec_()

    if entry_form.immigration_form:
        bot = BerlinImmigrationOfficeBot(entry_form.immigration_form)
    elif entry_form.citizen_service_url:
        bot = BerlinCitizenOfficeBot(entry_form.citizen_service_url)
    else:
        sys.exit()

    while True:
        try:
            bot.run_loop()
        except Exception as e:
            print(e)
            bot.play_sound(SOUND['error'])
            time.sleep(10)
