<img width="255" alt="Screenshot 2024-05-02 at 00 10 34" src="https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/assets/4144711/fea0cf5a-24ca-45ec-87ea-e779aa2fd275">

# Book a Berlin LEA appointment without wasting your precious time

No technical skills needed!

<a href="https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosapple.zip">
  <img src="resources/download-macos-apple-chip.png" alt="Download for macOS (apple chip)" width=400 />
</a>
<a href="https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosintel.zip">
  <img src="resources/download-macos-intel-chip.png" alt="Download for macOS (intel chip)" width=400 />
</a>

<br/>
<br/>
<div>
  <a href="https://www.loom.com/share/36408247f4234b4083509450a3db2928">
    <p>Watch demo</p>
  </a>
  <a href="https://www.loom.com/share/36408247f4234b4083509450a3db2928">
    <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/36408247f4234b4083509450a3db2928-with-play.gif">
  </a>
</div>


## What is this?

This bot helps you book an appointment from https://otv.verwalt-berlin.de/ams/TerminBuchen.
Without using a bot, you have to fill out the form every 10 minutes and constantly click the 'Next' button. It's INHUMANE. Even if you get to the date selection page, you probably can't book an appointment because someone else is faster than you, so you end up having to repeat the process endlessly. It should be a crime for the people who invented this!
This bot automates the manual steps for you. You just need to fill out the initial form once and run the bot. When you hear the alert and notification, proceed with the remaining steps manually (selecting the time, solving the reCAPTCHA, and entering your name, birthday, and email), and end your nightmare.

## How to use?

1. Download `berlin-termin-bot.zip`

   - [macOS (apple chip)](https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosapple.zip)
   - [macOS (intel chip)](https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/releases/download/v1.0.0/berlin-termin-bot_macosintel.zip)

2. Unzip the file
3. Right-click the program (`berlin-termin-bot`) and click 'Open' to run it (Don't double-click)
4. Fill out the form and click 'Good luck' button to start (see the screenshot below)
5. Wait for the alarm/notification
6. If you hear the alarm, rush to select the day and time and solve the reCAPTCHA. If the time dropdown is empty, it means it's gone. Go to the Terminal window and hit 'Enter' to start over.
7. Good luck!

<img width="783" alt="Screenshot 2024-04-30 at 00 08 11" src="https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/assets/4144711/e2bfd517-c2f3-4e60-9b62-d5829e91c3b9">

## Tips

You'll most likely get an appointment during working hours when they release new slots. Outside of working hours, you might occasionally see available time slots when people cancel their appointments, but it's nearly impossible to secure one. If you run the bot from 9 a.m. to 5 p.m., Monday to Friday, you should be able to get an appointment within 2-3 weeks. Cheer up!

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

## Support ❤️

<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4WQZ5PBVUVJ4A">
  <img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width=200 />
</a>
<br/>
<a href="https://www.buymeacoffee.com/chialunwu">
  <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=chialunwu&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" />
</a>
