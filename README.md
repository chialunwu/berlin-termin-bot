<img width="255" alt="Screenshot 2024-05-02 at 00 10 34" src="https://github.com/chialunwu/berlin-termin-bot/assets/4144711/fea0cf5a-24ca-45ec-87ea-e779aa2fd275">

# Book a Berlin LEA/Bürgeramt appointment without wasting your valuable time

No technical skills required!

<a href="https://github.com/chialunwu/berlin-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosapple.zip">
  <img src="resources/download-macos-apple-chip.png" alt="Download for macOS (apple chip)" width=400 />
</a>
<a href="https://github.com/chialunwu/berlin-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosintel.zip">
  <img src="resources/download-macos-intel-chip.png" alt="Download for macOS (intel chip)" width=400 />
</a>

<br/>
<a href="https://github.com/chialunwu/berlin-termin-bot/releases/download/v1.0.0/berlin-termin-bot.exe">
  <img src="resources/download-windows.png" alt="Download for Windows" width=300 />
</a>
<br/>

- _The Windows version may not work on your machine. Fix in-progress_ 🛠️
- _Special credits to [@ananaphasia](https://github.com/ananaphasia) for building the Windows version!_

<br/>

**IMPORTANT**: For booking an LEA appointment, did you try to send a request using https://www.berlin.de/einwanderung/en/services/appointments/artikel.1144334.en.php already? You might get an appointment earlier using that approach.

<br/>
<div>
    <a href="https://www.loom.com/share/7011a313f44347e6a205384fbd03a0be">
      <p>Watch demo</p>
    </a>
    <a href="https://www.loom.com/share/7011a313f44347e6a205384fbd03a0be">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/7011a313f44347e6a205384fbd03a0be-with-play.gif">
    </a>
  </div>

## What is this?

This bot assists you in booking an appointment from either https://otv.verwalt-berlin.de/ams/TerminBuchen or https://service.berlin.de/dienstleistung/.

Booking an LEA appointment without the bot involves filling out the form every 10 minutes and continually clicking the 'Next' button. It's an exhausting process. Even if you reach the date selection page, someone else may secure the appointment before you, leaving you to repeat the process over and over. The bot automates these manual steps for you. You just need to complete the initial form once and then run the bot. When you hear the alert and notification, proceed with the remaining steps manually (choosing the time, solving the reCAPTCHA, and entering your name, date of birth, and email) to finalize your appointment.

For booking a Bürgeramt appointment, while you don't need to complete a form beforehand, you still must frequently refresh the page, which can lead to being blocked for an hour if done too often. The bot refreshes the page every 60 seconds for you, streamlining the process.

## How to use?

### Prerequisites

- Install [Chrome](https://www.google.com/chrome)
- To keep the bot running, you might need to prevent your laptop from falling asleep. You can install software like [Caffeine](https://intelliscapesolutions.com/apps/caffeine) to keep your laptop awake.

### Get the bot

1. Download `berlin-termin-bot.zip`

   - [macOS (apple chip)](https://github.com/chialunwu/berlin-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosapple.zip)
   - [macOS (intel chip)](https://github.com/chialunwu/berlin-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosintel.zip)
   - [Windows](https://github.com/chialunwu/berlin-termin-bot/releases/download/v1.0.0/berlin-termin-bot.exe)
     - NOTE: The Windows version may not work on your machine. Fix in-progress 🛠️

2. Unzip the file
3. Right-click the program (`berlin-termin-bot`) and click `Open` to run it (Don't double-click). To run it next time, simply double-click.

<img width="476" alt="Screenshot 2024-05-09 at 23 37 08" src="https://github.com/chialunwu/berlin-termin-bot/assets/4144711/63d87b06-1114-48a4-bc16-ebdde0ed2357">

### Book an LEA appointment

#### !!IMPORTANT!!: You may not need to use this bot. Did you try to send a request to LEA using https://www.berlin.de/einwanderung/en/services/appointments/artikel.1144334.en.php ?

1. Click the `Immigration Office` button
2. Fill out the form and click `Start`
3. Wait for the alarm/notification
4. If you hear the alarm, rush to select the day and time and solve the reCAPTCHA. If the time dropdown is empty, it means it's gone. Go to the Terminal window and hit 'Enter' to start over.
5. Good luck!

<img width="783" alt="Screenshot 2024-04-30 at 00 08 11" src="https://github.com/chialunwu/berlin-termin-bot/assets/4144711/e2bfd517-c2f3-4e60-9b62-d5829e91c3b9">

#### 💡 Tips 💡

You'll most likely get an appointment during working hours when they release new slots. Outside of working hours, you might occasionally see available time slots when people cancel their appointments, but it's nearly impossible to secure one. If you run the bot from 9 a.m. to 5 p.m., Monday to Friday, you should be able to get an appointment within 2-3 weeks. Cheer up!

### Book an Anmeldung appointment

1. Click the `Anmeldung einer Wohnung` button
2. Wait for the alarm/notification
3. Good luck!

### Book a Bürgeramt appointment for additional services

1. Click the `Other Bürgeramt services` button
2. Enter the URL
   - For example, for the service - https://service.berlin.de/dienstleistung/120686/, right-click the `Berlinweite Terminbuchung` button and click `Copy Link Address`.
     <img width="1439" alt="Screenshot 2024-05-09 at 23 10 11" src="https://github.com/chialunwu/berlin-termin-bot/assets/4144711/6be0500d-654c-40f6-8436-f97603a281e4">
3. Wait for the alarm/notification
4. Good luck!

<img width="500" alt="Screenshot 2024-05-10 at 13 15 48" src="https://github.com/chialunwu/berlin-termin-bot/assets/4144711/13718573-1d85-476c-9b5b-f38a3b382110">

## Development

### Build

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Run

```bash
python3 berlin-termin-bot.py
```

## ❤️ Support ❤️

<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4WQZ5PBVUVJ4A">
  <img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width=200 />
</a>
<br/>
<a href="https://www.buymeacoffee.com/chialunwu">
  <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=chialunwu&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" />
</a>
