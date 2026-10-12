# Brave Origin-like for Windows

This script configures the standard version of Brave to align as closely as possible with the Brave Origin philosophy of "disabling everything except core features."

## Files

- `main.ps1` — Main script
- `run.cmd` — Launcher (run by double-clicking)

## Usage

### Applying the configuration

Right-click `run.cmd` and select "Run as administrator."

Alternatively, a standard double-click will also trigger a prompt to elevate to administrator privileges.

### Reverting changes

`run.cmd /undo`

Or via Command Prompt:

```text
run.cmd /undo
```

### Checking status

```text
run.cmd /status
```

## Features Disabled

In accordance with the official Brave Origin description, the following features are disabled:

- Rewards / Brave Ads
- Wallet / Web3
- VPN
- Leo AI
- News
- Talk
- Tor
- P3A
- Daily usage / Stats Ping
- Web Discovery Project
- Speedreader
- Wayback Machine
- Playlist
- Email aliases

## Features Intentionally Retained

The following are considered core Origin features or standard browser functions, so this script does not disable them:

- Brave Shields
- Chromium security features
- Safe Browsing
- JavaScript
- Cookies
- Extensions
- Password manager
- Autofill
- Sync

## Notes

Because this script sets Brave management policies in HKLM, Brave may display the message:
"Managed by your organization"
This is expected behavior for this method.

Also, this script does not remove the features themselves from the Brave executable file.
Unlike the standalone version of Brave Origin, the unnecessary features remain in the binary. After applying the changes, fully close and restart Brave, then verify the policies at `brave://policy`.
