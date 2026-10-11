import time
import os
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

button_pressed = False

while True:
    if GPIO.input(7) == GPIO.HIGH and not button_pressed:
        print("Someone pressed the alert button!")

        try:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": CHAT_ID,
                    "text": "Someone pressed the alert button!"
                },
                timeout=10
            )
            response.raise_for_status()
            print("Telegram alert sent!")
        except requests.RequestException as e:
            print("Telegram error:", e)

        button_pressed = True

    if GPIO.input(7) == GPIO.LOW:
        button_pressed = False

    time.sleep(0.1)
