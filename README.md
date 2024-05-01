
<img width="255" alt="Screenshot 2024-05-02 at 00 10 34" src="https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/assets/4144711/fea0cf5a-24ca-45ec-87ea-e779aa2fd275">


## What is this?

This bot helps you book an appointment from https://otv.verwalt-berlin.de/ams/TerminBuchen.
Without using a bot, you have to fill out the form every 10 minutes and constantly click the 'Next' button. It's INHUMANE. Even if you get to the date selection page, you probably can't book an appointment because someone else is faster than you, so you end up having to repeat the process endlessly. It should be a crime for the people who invented this!
This bot automates the manual steps for you. You just need to fill out the initial form once and run the bot. When you hear the alert and notification, proceed with the remaining steps manually (selecting the time, solving the reCAPTCHA, and entering your name, birthday, and email), and end your nightmare.

## How to use?

1. Download `berlin-termin-bot.zip` in [downloads](downloads/macos)
   - macOS only
   - For Windows users, please see the 'Development' section below
2. Unzip the file
3. Right-click the program and click 'Open' to run it (Don't double-click)
4. Fill out the form and click 'Good luck' button to start (see the screenshot below)
5. Wait for the alarm/notification
6. Good luck!

<img width="783" alt="Screenshot 2024-04-30 at 00 08 11" src="https://github.com/chialunwu/berlin-auslanderbehorde-termin-bot/assets/4144711/e2bfd517-c2f3-4e60-9b62-d5829e91c3b9">

## Development

### To build

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### To run

```
python3 berlin-termin-bot.py
```

### To package

```
rm -rf dist build
rm -f downloads/macos/applechip/*
pyinstaller --paths venv/lib/python3.11/site-packages/ \
    --onefile \
    --add-data="*.mp3:." \
    berlin-termin-bot.py
cd dist
zip -r ../downloads/macos/applechip/berlin-termin-bot.zip berlin-termin-bot
cd ..
```
