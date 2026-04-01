<div align="center">

<pre>
        ___
       __H__
 ___ ___[.]_____ ___ ___
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V          |_|

     sqlinject  by  flandreiii
       easier sql injection
</pre>

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux-green?style=for-the-badge&logo=linux&logoColor=white)
![sqlmap](https://img.shields.io/badge/Powered%20by-sqlmap-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

**A Python wrapper around sqlmap that makes SQL injection testing faster and easier.**

Interactive menu · 9 scan modes · Clean color output · No flag memorization needed

**Creator:** [flandreiii](https://github.com/flandreiii) &nbsp;·&nbsp; **Tested on:** CachyOS · Kali Linux · Termux

</div>

---

## What is sqlinject?

sqlinject is a command-line tool that wraps [sqlmap](https://sqlmap.org/) with a friendly interactive menu and simple CLI flags. Instead of memorizing long sqlmap commands, you just pick a mode and enter a URL.

Works on:
- **CachyOS** (Arch-based, Hyprland)
- **Kali Linux** (sqlmap pre-installed)
- **Termux** (Android, native + Kali proot)

---

## Requirements

- Python 3.10+
- sqlmap

### Install sqlmap

```bash
# CachyOS / Arch Linux
sudo pacman -S python sqlmap

# Kali Linux / Debian / Ubuntu
sudo apt install python3 sqlmap

# Termux (Android)
pkg update && pkg install python sqlmap
```

---

## Installation

```bash
# Clone the repo
git clone https://github.com/flandreiii/sqlinject
cd sqlinject

# Make executable
chmod +x sqlinject.py

# Optional: install globally
sudo cp sqlinject.py /usr/local/bin/sqlinject
```

---

## Usage

### Interactive menu (recommended)

```bash
python3 sqlinject.py
```

### CLI mode

```bash
python3 sqlinject.py -u "http://target.com/page?id=1" -m quick
```

---

## Modes

| Mode | Description | CLI Example |
|------|-------------|-------------|
| `quick` | Detect SQL injection on a URL | `-u "URL" -m quick` |
| `dbs` | List all databases | `-u "URL" -m dbs` |
| `tables` | List tables in a database | `-u "URL" -m tables -D mydb` |
| `dump` | Extract data from a table | `-u "URL" -m dump -D mydb -T users` |
| `forms` | Auto-scan all forms on a page | `-u "URL" -m forms` |
| `post` | Test POST parameters | `-u "URL" -m post --data "user=a&pass=b"` |
| `cookie` | Test cookie-based injection | `-u "URL" -m cookie --cookie "id=1"` |
| `crawl` | Crawl a site and test all URLs | `-u "URL" -m crawl --depth 3` |
| `shell` | Try to get an OS shell | `-u "URL" -m shell` |

---

## Examples

```bash
# Quick scan
python3 sqlinject.py -u "http://testsite.com/item?id=1" -m quick

# List databases
python3 sqlinject.py -u "http://testsite.com/item?id=1" -m dbs

# Dump a table
python3 sqlinject.py -u "http://testsite.com/item?id=1" -m dump -D shop -T users

# Scan a login form
python3 sqlinject.py -u "http://testsite.com/login" -m forms

# Test a POST request
python3 sqlinject.py -u "http://testsite.com/login" -m post --data "username=admin&password=test"

# Cookie injection
python3 sqlinject.py -u "http://testsite.com/profile" -m cookie --cookie "user_id=3"

# Use with Tor
python3 sqlinject.py -u "http://testsite.com/item?id=1" -m quick --extra --tor --tor-type=SOCKS5
```

---

## Platform Notes

### CachyOS (Arch-based)

```bash
sudo pacman -S python sqlmap
python3 sqlinject.py
```

Works natively. Compatible with kitty, foot, alacritty and any Hyprland terminal.

### Kali Linux

```bash
# sqlmap is pre-installed on Kali
python3 sqlinject.py
```

Works out of the box. If sqlmap is missing: `sudo apt install sqlmap`

### Termux (Android)

```bash
pkg update && pkg install python sqlmap
python3 sqlinject.py
```

Works natively in Termux and inside Kali proot-distro.

---

## Disclaimer

> sqlinject is intended **only** for authorized penetration testing and security research.
> Only use this tool on systems you own or have explicit written permission to test.
> Unauthorized use is illegal and unethical. The creator holds no responsibility for misuse.

---

## Support

If this tool helped you, consider buying me a coffee!

<div align="center">

<a href="https://buymeacoffee.com/flandreiii">
  <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" />
</a>

</div>

---

<div align="center">

`#termux` &nbsp; `#kalilinux` &nbsp; `#cachyos` &nbsp; `#sqlinjection` &nbsp; `#pentesting` &nbsp; `#sqlmap` &nbsp; `#cybersecurity` &nbsp; `#ethicalhacking` &nbsp; `#linux` &nbsp; `#python`

</div>
