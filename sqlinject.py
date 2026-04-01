#!/usr/bin/env python3
# sqlinject - Easy SQL Injection Tool
# Creator: flandreiii
# Wrapper around sqlmap for easier usage

import subprocess
import sys
import os
import shutil
import argparse
from datetime import datetime

# ─────────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────────
R  = "\033[1;31m"
G  = "\033[1;32m"
Y  = "\033[1;33m"
B  = "\033[1;34m"
C  = "\033[1;36m"
W  = "\033[1;37m"
M  = "\033[1;35m"
DG = "\033[0;90m"
NC = "\033[0m"

# ─────────────────────────────────────────────
#  LOGO (sqlmap-style)
# ─────────────────────────────────────────────
LOGO = f"""
{R}        ___
{R}       __H__
{R} ___ ___[{Y},{R}]_____ ___ ___  {{1.0}}
{R}|_ -| . [{Y}({R}]     | .'| . |
{R}|___|_  [{Y}){R}]_|_|_|__,|  _|
{R}      |_|V...       |_|   {NC}
{DG}       {W}sqlinject {DG}by {C}flandreiii{NC}
{DG}       easier sql injection{NC}
"""

SEPARATOR = f"{DG}{'─' * 55}{NC}"

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def banner():
    print(LOGO)
    print(SEPARATOR)

def info(msg):
    print(f"{B}[*]{NC} {msg}")

def ok(msg):
    print(f"{G}[+]{NC} {msg}")

def warn(msg):
    print(f"{Y}[!]{NC} {msg}")

def err(msg):
    print(f"{R}[-]{NC} {msg}")

def check_sqlmap():
    if shutil.which("sqlmap") is None:
        err("sqlmap not found!")
        print(f"    {Y}Install it:{NC}")
        print(f"      {DG}# Kali / Debian:{NC}  sudo apt install sqlmap")
        print(f"      {DG}# Arch / CachyOS:{NC} sudo pacman -S sqlmap")
        print(f"      {DG}# Termux:{NC}          pkg install sqlmap")
        sys.exit(1)
    ok("sqlmap found")

def run_sqlmap(args_list: list[str]):
    cmd = ["sqlmap"] + args_list
    info(f"Running: {DG}{' '.join(cmd)}{NC}")
    print(SEPARATOR)
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted.{NC}")

# ─────────────────────────────────────────────
#  MODES
# ─────────────────────────────────────────────

def mode_quick(url: str, extra: list[str]):
    """Quick scan – detect injection on a URL."""
    info(f"Quick scan on: {C}{url}{NC}")
    args = [
        "-u", url,
        "--batch",          # no interactive prompts
        "--level", "3",
        "--risk", "2",
        "--banner",
    ] + extra
    run_sqlmap(args)

def mode_dump(url: str, db: str | None, table: str | None, extra: list[str]):
    """Dump database / table."""
    info(f"Dump mode on: {C}{url}{NC}")
    args = ["-u", url, "--batch", "--level", "3", "--risk", "2"]
    if db:
        args += ["--dbms", "auto", "-D", db]
    if table:
        args += ["-T", table, "--dump"]
    else:
        args += ["--dump-all"]
    args += extra
    run_sqlmap(args)

def mode_dbs(url: str, extra: list[str]):
    """List databases."""
    info(f"Listing databases on: {C}{url}{NC}")
    args = ["-u", url, "--batch", "--dbs"] + extra
    run_sqlmap(args)

def mode_tables(url: str, db: str, extra: list[str]):
    """List tables in a database."""
    info(f"Listing tables in DB '{C}{db}{NC}'")
    args = ["-u", url, "--batch", "-D", db, "--tables"] + extra
    run_sqlmap(args)

def mode_shell(url: str, extra: list[str]):
    """Try to get an OS shell."""
    warn("OS shell mode – use only on authorized targets!")
    args = ["-u", url, "--os-shell"] + extra
    run_sqlmap(args)

def mode_forms(url: str, extra: list[str]):
    """Auto-detect and test forms on a page."""
    info(f"Scanning forms on: {C}{url}{NC}")
    args = ["-u", url, "--forms", "--batch", "--level", "3", "--risk", "2"] + extra
    run_sqlmap(args)

def mode_post(url: str, data: str, extra: list[str]):
    """Test a POST request."""
    info(f"POST scan on: {C}{url}{NC}")
    info(f"Data: {DG}{data}{NC}")
    args = ["-u", url, "--data", data, "--batch", "--level", "3", "--risk", "2"] + extra
    run_sqlmap(args)

def mode_cookie(url: str, cookie: str, extra: list[str]):
    """Test cookie-based injection."""
    info(f"Cookie injection on: {C}{url}{NC}")
    args = ["-u", url, "--cookie", cookie, "--level", "2", "--batch"] + extra
    run_sqlmap(args)

def mode_crawl(url: str, depth: int, extra: list[str]):
    """Crawl a site and test all found URLs."""
    info(f"Crawling: {C}{url}{NC} (depth={depth})")
    args = ["-u", url, "--crawl", str(depth), "--batch", "--level", "2", "--risk", "1"] + extra
    run_sqlmap(args)

# ─────────────────────────────────────────────
#  INTERACTIVE MENU
# ─────────────────────────────────────────────

def interactive():
    print(f"\n{W}Select a mode:{NC}")
    modes = [
        ("1", "Quick Scan",        "Detect SQLi on a URL"),
        ("2", "List Databases",    "Show all databases"),
        ("3", "List Tables",       "Show tables in a DB"),
        ("4", "Dump Data",         "Extract table data"),
        ("5", "Form Scan",         "Auto-scan page forms"),
        ("6", "POST Scan",         "Test POST parameters"),
        ("7", "Cookie Injection",  "Test cookie fields"),
        ("8", "Crawl & Scan",      "Crawl site and test all URLs"),
        ("9", "OS Shell",          "Try OS shell (authorized only)"),
    ]
    for num, name, desc in modes:
        print(f"  {Y}[{num}]{NC} {W}{name:<22}{NC} {DG}{desc}{NC}")

    print()
    choice = input(f"{C}sqlinject>{NC} ").strip()

    if choice not in [str(i) for i in range(1, 10)]:
        err("Invalid choice.")
        return

    url = input(f"{B}Target URL:{NC} ").strip()
    if not url:
        err("URL required.")
        return

    extra_str = input(f"{DG}Extra sqlmap flags (optional, e.g. --tor --proxy http://...):{NC} ").strip()
    extra = extra_str.split() if extra_str else []

    print()

    if choice == "1":
        mode_quick(url, extra)
    elif choice == "2":
        mode_dbs(url, extra)
    elif choice == "3":
        db = input(f"{B}Database name:{NC} ").strip()
        mode_tables(url, db, extra)
    elif choice == "4":
        db    = input(f"{B}Database (leave empty for all):{NC} ").strip() or None
        table = input(f"{B}Table (leave empty for all):{NC} ").strip() or None
        mode_dump(url, db, table, extra)
    elif choice == "5":
        mode_forms(url, extra)
    elif choice == "6":
        data = input(f"{B}POST data (e.g. user=test&pass=test):{NC} ").strip()
        mode_post(url, data, extra)
    elif choice == "7":
        cookie = input(f"{B}Cookie string (e.g. PHPSESSID=abc123):{NC} ").strip()
        mode_cookie(url, cookie, extra)
    elif choice == "8":
        depth = input(f"{B}Crawl depth (default 2):{NC} ").strip()
        depth = int(depth) if depth.isdigit() else 2
        mode_crawl(url, depth, extra)
    elif choice == "9":
        mode_shell(url, extra)

# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        prog="sqlinject",
        description="sqlinject – easy SQLi wrapper by flandreiii",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True,
    )
    p.add_argument("-u", "--url",    help="Target URL")
    p.add_argument("-m", "--mode",   help=(
        "Mode:\n"
        "  quick   – detect injection\n"
        "  dbs     – list databases\n"
        "  tables  – list tables (-D required)\n"
        "  dump    – dump data\n"
        "  forms   – scan page forms\n"
        "  post    – test POST (--data required)\n"
        "  cookie  – test cookie (--cookie required)\n"
        "  crawl   – crawl and scan\n"
        "  shell   – OS shell"
    ))
    p.add_argument("-D", "--db",     help="Database name")
    p.add_argument("-T", "--table",  help="Table name")
    p.add_argument("--data",         help="POST data string")
    p.add_argument("--cookie",       help="Cookie string")
    p.add_argument("--depth",        type=int, default=2, help="Crawl depth (default: 2)")
    p.add_argument("--extra",        nargs=argparse.REMAINDER, default=[], help="Extra flags passed to sqlmap")
    return p

def main():
    banner()
    check_sqlmap()

    parser = build_parser()
    args   = parser.parse_args()

    # no args → interactive
    if not args.url and not args.mode:
        interactive()
        return

    if not args.url:
        err("URL required (-u / --url).")
        parser.print_help()
        sys.exit(1)

    mode  = (args.mode or "quick").lower()
    extra = args.extra or []

    if mode == "quick":
        mode_quick(args.url, extra)
    elif mode == "dbs":
        mode_dbs(args.url, extra)
    elif mode == "tables":
        if not args.db:
            err("--db / -D required for tables mode.")
            sys.exit(1)
        mode_tables(args.url, args.db, extra)
    elif mode == "dump":
        mode_dump(args.url, args.db, args.table, extra)
    elif mode == "forms":
        mode_forms(args.url, extra)
    elif mode == "post":
        if not args.data:
            err("--data required for post mode.")
            sys.exit(1)
        mode_post(args.url, args.data, extra)
    elif mode == "cookie":
        if not args.cookie:
            err("--cookie required for cookie mode.")
            sys.exit(1)
        mode_cookie(args.url, args.cookie, extra)
    elif mode == "crawl":
        mode_crawl(args.url, args.depth, extra)
    elif mode == "shell":
        mode_shell(args.url, extra)
    else:
        err(f"Unknown mode: {mode}")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
