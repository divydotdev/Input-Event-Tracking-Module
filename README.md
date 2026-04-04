<table width="100%">
<tr>
<td align="center">

<div align="center">

# 🔒 Input-Event-Tracking-Module

</div>

<p align="center">An educational demonstration module that collects keyboard events, active-application context, screenshots, system info and (optionally) webcam frames. This repo is intended for controlled, consented classroom or lab use only.</p>

</td>
</tr>
</table>

<div align="center">╭──────────── ✦ ────────────╮</div>

✨ Why this README looks different

- Clear, modern layout for presentations
- Strong safety, legal & consent warnings up front
- Quick start steps and a safe demo path so you can show results without capturing real users

<div align="center">╰──────────── ✦ ────────────╯</div>

⚠️ Legal & Ethical Notice

Keylogging and recording users' activity can be illegal and violate privacy in many jurisdictions. Do NOT run this script on any system you do not own or without explicit, documented consent from everyone involved. This repository is provided for educational purposes only — improper use is your responsibility.

<div align="center">╭──────────── ✦ ────────────╮</div>

🚨 Quick Safety Checklist (read before running)

- Use a disposable Windows VM or isolated lab machine.
- Notify and obtain written consent from participants.
- Use test-only email accounts for any SMTP credentials.
- Consider disabling network access to prevent data exfiltration during demos.

<div align="center">╰──────────── ✦ ────────────╯</div>

🚀 Quick Start (recommended: disposable Windows VM)

1. Copy `.env.example` to `.env` and populate values locally (do NOT commit `.env`).

2. Create and activate a Python virtual environment and install dependencies:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1    # PowerShell
# or: .\\.venv\\Scripts\\activate.bat  # cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Populate `.env` with test values (or leave SMTP fields empty to skip sending).

4. Run (inside the VM):

```powershell
python Keylogger.py
```

<div align="center">╭──────────── ✦ ────────────╮</div>

🎯 Recommended Safe Demo Modes

Use one of these to present results without recording real users:

- Demo Mode (manual): Before running, edit `Keylogger.py` and comment out calls to `keyboard.on_press`, `screenshot()` and `capture_camera()` and instead write simulated entries into `document.txt` and `applicationLog.txt`.
- Network-disabled demo: Disconnect the VM from the network or block outbound SMTP so data is never transmitted.
- Simulated-data script: I can add a `--demo` or `TEST_MODE` flag that populates sample data and skips all hardware/network capture — tell me if you want this added.

<div align="center">╰──────────── ✦ ────────────╯</div>

Files of interest

- `Keylogger.py` — main script that captures events and sends attachments via SMTP
- `.env.example` — example env variables (copy to `.env` and fill locally)
- `requirements.txt` — Python dependencies

<div align="center">╭──────────── ✦ ────────────╮</div>

Configuration notes

- `.env` variables (copy from `.env.example`):

```
EMAIL_SENDER=sender@example.com
EMAIL_RECEIVER=receiver@example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
EMAIL_USERNAME=user@example.com
EMAIL_PASSWORD=your_app_password_here
```

- If you leave these blank, the script will skip email sending.

========================

Best practices for your presentation

- Prepare a short slide that explains legality and consent before the demo.
- Use prerecorded/simulated input for the live demo to avoid privacy risks.
- Show `document.txt`, `applicationLog.txt`, `syseminfo.txt`, and the generated images as the outputs.

========================

Want me to add a safe `--demo` flag?

If you'd like, I can update `Keylogger.py` to provide a `--demo` mode that disables live capture and sending and instead generates deterministic sample output for a risk-free presentation. Reply "Add demo mode" and I'll implement it.

========================

Credits & License

This project is educational. Use responsibly.
