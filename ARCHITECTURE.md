<table width="100%">
<tr>
<td align="center">

<div align="center">

# 🏗️ Architecture — Input-Event-Tracking-Module

</div>

This document describes the system architecture, component structure, and data flow of the Input-Event-Tracking-Module.

</td>
</tr>
</table>

<div align="center">╭──────────── ✦ ────────────╮</div>

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Input-Event-Tracking-Module                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Keyboard    │  │  Screenshot  │  │   Webcam     │           │
│  │  Capture     │  │  Capture     │  │  Capture     │           │
│  └─────┬────────┘  └─────┬────────┘  └─────┬────────┘           │
│        │                 │                 │                     │
│        └─────────────────┼─────────────────┘                     │
│                          │                                       │
│              ┌───────────▼────────────┐                          │
│              │  Data Processing      │                          │
│              │  & Aggregation        │                          │
│              └───────────┬────────────┘                          │
│                          │                                       │
│        ┌─────────────────┼─────────────────┐                     │
│        │                 │                 │                     │
│   ┌────▼────┐     ┌──────▼──────┐   ┌─────▼────┐               │
│   │document │     │application  │   │syseminfo │               │
│   │.txt     │     │Log.txt      │   │.txt      │               │
│   └────┬────┘     └──────┬──────┘   └─────┬────┘               │
│        │                 │                │                     │
│        └─────────────────┼────────────────┘                     │
│                          │                                       │
│              ┌───────────▼────────────┐                          │
│              │  Email Module          │                          │
│              │  (SMTP Integration)    │                          │
│              └────────────────────────┘                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. **Input Capture Subsystem**

#### 1.1 Keyboard Capture
- **Module**: `keyboard` library (pypi)
- **Function**: `capture_keys()`
- **Purpose**: Real-time keystroke monitoring
- **Mechanism**: 
  - Registers global keyboard event listener
  - Callback function triggered on each key press
  - Buffers keys in memory before writing to disk

#### 1.2 Screenshot Capture
- **Module**: `PIL.ImageGrab` (Pillow)
- **Function**: `screenshot()`
- **Purpose**: Periodic screen capture
- **Mechanism**:
  - Grabs entire screen framebuffer
  - Encodes to PNG format
  - Saves to disk

#### 1.3 Webcam Capture
- **Module**: `cv2.VideoCapture` (OpenCV)
- **Function**: `capture_camera()`
- **Purpose**: Webcam frame extraction
- **Mechanism**:
  - Opens default camera device (index 0)
  - Reads single frame
  - Encodes to PNG format
  - Releases camera resource

#### 1.4 System Information Gathering
- **Module**: `platform`, `socket`, `requests`, `psutil`
- **Function**: `computer_information()`
- **Purpose**: System profiling and identification
- **Gathered Data**:
  - Hostname and IP addresses (private + public)
  - Processor information
  - Operating System details
  - Machine architecture

---

### 2. **Application Context Tracking**

#### 2.1 Active Application Monitor
- **Module**: `win32gui` (PyWin32)
- **Function**: `get_active_app_name()`
- **Purpose**: Identify active window/application
- **Mechanism**:
  - Queries Windows foreground window handle
  - Retrieves window title text
  - Logs with timestamp correlation

#### 2.2 Application Log
- **Data Structure**: Dictionary `active_apps`
- **Content**: `{timestamp: active_app_name}`
- **Function**: `write_application_log()`
- **Output**: `applicationLog.txt`

---

### 3. **Data Storage Subsystem**

#### 3.1 File-Based Storage
| File | Purpose | Format | Trigger |
|------|---------|--------|---------|
| `document.txt` | Captured keystrokes | Plain text | Every 5 seconds |
| `applicationLog.txt` | Active app context | Text (timestamp, app) | Every 5 seconds |
| `syseminfo.txt` | System metadata | Text key-value | On startup |
| `screenshot.png` | Screen capture | PNG image | Before email send |
| `webcam.png` | Webcam frame | PNG image | Before email send |

#### 3.2 File Access Safety
- **Function**: `ensure_file_access(path)`
- **Behavior**:
  - Creates file if missing
  - Verifies read/write permissions
  - Returns boolean success status
  - Graceful error handling

---

### 4. **Communication Subsystem**

#### 4.1 Email Module (`send_email()`)
- **Protocol**: SMTP (Simple Mail Transfer Protocol)
- **Configuration Source**: Environment variables (`.env` file)
- **Required Variables**:
  ```
  EMAIL_SENDER
  EMAIL_RECEIVER
  SMTP_SERVER
  SMTP_PORT
  EMAIL_USERNAME
  EMAIL_PASSWORD
  ```

#### 4.2 Message Construction
- **Type**: `MIMEMultipart` (MIME format)
- **Attachments**:
  - `document.txt` (captured keystrokes)
  - `applicationLog.txt` (app context)
  - `syseminfo.txt` (system info)
  - `screenshot.png` (screen capture)
  - `webcam.png` (webcam frame)

#### 4.3 Send Mechanisms
- **SSL (port 465)**: Secure connection with `SMTP_SSL`
- **TLS (port 587)**: STARTTLS encryption upgrade
- **Error Handling**: 
  - Authentication failure detection
  - Gmail App Password guidance
  - Network error handling

---

### 5. **Execution Control Subsystem**

#### 5.1 Main Capture Loop (`capture_keys()`)
```
while True:
    elapsed_time = time.time() - start_time
    if elapsed_time >= 5 seconds:
        write_to_file()          # Flush keystroke buffer
        write_application_log()  # Log active applications
        send_email()             # Transmit data
        start_time = reset()     # Reset timer
```

#### 5.2 Demo Mode (`demo_mode()`)
- **Purpose**: Safe educational simulation
- **Behavior**:
  - Creates synthetic keystroke data
  - Generates demo application logs
  - Creates demo images (without real capture)
  - No keyboard hooks activated
  - No network transmission

#### 5.3 Command-Line Interface
```python
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo')              # Enable demo mode
    parser.add_argument('--demo-iterations')   # Number of iterations
    parser.add_argument('--demo-interval')     # Seconds between iterations
```

---

## Data Flow Diagram

### Live Mode (Production)
```
System Events
    │
    ├─► Keyboard Event ──────┐
    │                        │
    ├─► Screen ─────────────┤
    │                        ├─► Aggregation ──► Files ──► Email Sender ──► SMTP Server
    │                        │
    └─► Webcam ────────────┤
                           │
    Active App Context ───┤
    System Info ─────────┘
```

### Demo Mode (Educational)
```
Synthetic Data Generation
    │
    ├─► Mock Keystrokes ────┐
    │                       │
    ├─► Demo Images ───────┤──► File Write ──► Local Output
    │                       │
    └─► Demo System Info ──┘
```

---

## Dependency Graph

```
Keylogger.py
├── keyboard                       # Keyboard event hooking
├── PIL (Pillow)                  # Screenshot & image creation
├── cv2 (OpenCV)                  # Webcam capture
├── pywin32                        # Windows GUI access
├── python-dotenv                 # Environment variable loading
├── smtplib (stdlib)              # Email transmission
├── requests                       # HTTP requests (public IP)
├── platform, socket, psutil      # System info gathering
└── argparse (stdlib)             # CLI argument parsing
```

---

## Module Interaction Matrix

| Module | Keyboard | Screenshot | Webcam | App Log | Email | System Info |
|--------|----------|-----------|--------|---------|-------|-------------|
| Keyboard Listener | Primary | - | - | Supporting | - | - |
| Screenshot | - | Primary | - | - | Input | - |
| Webcam | - | - | Primary | - | Input | - |
| App Context | Supporting | - | - | Primary | - | - |
| Email Sender | Input | Input | Input | Input | Primary | Input |
| System Info | - | - | - | - | Input | Primary |

---

## Security & Access Model

### Privilege Requirements
- **Keyboard Hooking**: Requires elevated privileges (Admin/Root)
- **Screenshot**: User-level access (current user's desktop)
- **Webcam**: Requires device permission (OS-level)
- **Windows API (win32gui)**: User-level
- **Network (SMTP)**: Standard user-level outbound

### Encryption & Protection
- **In-Transit**: SMTP over SSL/TLS (configurable)
- **At-Rest**: Plain text files (no built-in encryption)
- **Credentials**: Environment variables (must protect `.env` file)

### Detection Surface
- **Process Name**: Could be renamed/obfuscated
- **Window Title**: May be monitored by EDR/AV
- **Network Traffic**: SMTP outbound connections are visible
- **File I/O**: Log files created locally (detectable)
- **Registry**: Can be monitored on Windows

---

## Performance Considerations

### Memory Usage
- **Keyboard Buffer**: Grows with keystroke rate (~1-5 KB per 5 seconds)
- **Image Storage**: ~50-200 KB per screenshot/webcam frame
- **Active App Dict**: Minimal (~1-10 KB)

### CPU Usage
- **Keyboard Listener**: Low (event-driven)
- **Screenshot**: Moderate spike (every email send)
- **Webcam**: Moderate spike (every email send)
- **Email**: Moderate (SMTP negotiation)

### I/O Patterns
- **Keyboard Log**: Sequential append every 5 seconds
- **Screenshot**: Periodic writes (on email send)
- **Network**: Outbound SMTP connection every 5 seconds

---

## Configuration & Customization Points

### Timing
- **Capture Interval**: Currently hardcoded `5 seconds`
- **Demo Interval**: Configurable via CLI

### Network
- **SMTP Parameters**: Fully configurable via `.env`
- **Email Attachments**: Selectively configurable

### Capture Behavior
- **Keyboard Filtering**: Could whitelist/blacklist keys
- **Screenshot Quality**: Configurable compression ratio
- **Webcam Resolution/FPS**: Configurable via cv2 parameters

### Obfuscation (Future)
- **Process Hiding**: Registry/service manipulation
- **File Hiding**: Alternate Data Streams (ADS) on NTFS
- **Network Encryption**: Custom SSL certificates

---

## Testing Strategy

### Unit Testing
- File I/O functions (`ensure_file_access`)
- Data format validation
- Email message construction

### Integration Testing
- Keyboard → File pipeline
- Screenshot/Webcam capture chain
- Email transmission with attachments

### End-to-End Testing
- Full capture loop (keyboard, screen, email)
- Demo mode correctness
- Error recovery (network failure, permission denied)

---

## Scalability & Limitations

### Current Limitations
- **Single-User**: Only monitors one user per instance
- **Single-Monitor**: Screenshot covers primary display only
- **Single-Email**: All data funneled to one receiver
- **Local Processing**: No cloud or distributed storage
- **Windows-Centric**: Keyboard/screenshot heavily Windows-focused

### Scalability Opportunities
- **Multi-Instance**: Run multiple monitors on same system
- **Database Backend**: Replace file storage with SQLite/PostgreSQL
- **Distributed Logging**: Send data to central server
- **Cloud Integration**: S3/Azure Blob for large file storage

---

## Security Implications & Recommendations

### For Defenders (Detecting This Tool)
- Monitor for `keyboard` library imports
- Alert on `SMTP_SSL` or `STARTTLS` outbound
- Block registry modifications (persistence mechanisms)
- EDR/XDR rules targeting `cv2.VideoCapture(0)`, `ImageGrab`

### For Operators (Using This Tool Legally/Educationally)
- Use `.env` with strict file permissions (chmod 600)
- Run in isolated network segments
- Log all usage and receive approval
- Disable features not needed (email, webcam, etc.)

---

## Future Architecture Enhancements

- **Database Tier**: SQLite/PostgreSQL for persistent storage
- **Web API**: Flask/FastAPI for remote access
- **WebSocket**: Real-time streaming via Socket.IO
- **Cloud Storage**: Azure Blob/AWS S3 integration
- **Encryption Layer**: AES encryption for captured data
- **Authentication**: OAuth2 for web dashboard access

---

**Last Updated**: April 2026  
**Architecture Version**: 1.0  
**Compatibility**: Python 3.8+, Windows 10/11
