<table width="100%">
<tr>
<td align="center">

<div align="center">

# Implemented Features

</div>

This file summarizes the features that are currently implemented in the project.

</td>
</tr>
</table>

<div align="center">╭──────────── ✦ ────────────╮</div>

## Core Capture Features

- Keyboard event capture using the `keyboard` library.
- Buffering of captured keystrokes and periodic writing to `document.txt`.
- Active application tracking using `win32gui` and logging to `applicationLog.txt`.
- Screenshot capture saved to `screenshot.png`.
- Webcam frame capture saved to `webcam.png`.
- System information collection written to `syseminfo.txt`.

## Data Handling

- File access checks through `ensure_file_access()`.
- Automatic creation of missing output files when needed.
- Periodic flushing of captured data every 5 seconds.

## Email Sending

- SMTP email construction with multipart attachments.
- Attachment support for:
  - `document.txt`
  - `applicationLog.txt`
  - `syseminfo.txt`
  - `screenshot.png`
  - `webcam.png`
- Support for both SSL and TLS SMTP connections.
- Environment-based configuration loaded from `.env`.
- Graceful handling when required email variables are missing.
- Basic SMTP error handling for authentication and transport failures.

## Reliability and Safety Checks

- Webcam capture fallback when the camera is unavailable.
- Graceful handling of screenshot, webcam, and email failures.
- Public IP lookup with a fallback message when the network is unavailable.

## Output Files

The current implementation produces the following files:

- `document.txt`
- `applicationLog.txt`
- `syseminfo.txt`
- `screenshot.png`
- `webcam.png`

## Notes

- The repository documentation mentions demo-oriented ideas, but the current code does not expose a dedicated command-line demo mode.
- The helper `_write_demo_syseminfo()` exists in the script, but it is not wired into the main execution flow.
