import os
import sys
import time
import random
import subprocess
import shutil
import argparse
import termcolor
from importlib import resources
from pathlib import Path
from datetime import datetime
from termcolor import colored

default_scripts = os.path.expanduser("~/hashCrack")
default_windows_scripts = f"/c/Users/{os.getenv('USER')}/source/repos/ente0/hashCrack/scripts/windows"

def define_default_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Linux",
        "default_restorepath": os.path.expanduser("~/.local/share/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": "/usr/share/wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "8",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "1"
    }

def define_windows_parameters():
    return {
        "default_hashcat": ".",
        "default_status_timer": "y",
        "default_workload": "3",
        "default_os": "Windows",
        "default_restorepath": os.path.expanduser("~/hashcat/sessions"),
        "default_session": datetime.now().strftime("%Y-%m-%d"),
        "default_wordlists": f"/c/Users/{os.getenv('USER')}/wordlists",
        "default_masks": "masks",
        "default_rules": "rules",
        "default_wordlist": "rockyou.txt",
        "default_mask": "?d?d?d?d?d?d?d?d",
        "default_rule": "T0XlCv2.rule",
        "default_min_length": "8",
        "default_max_length": "16",
        "default_hashmode": "22000",
        "default_device": "1"
    }

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

import shutil
from termcolor import colored

def print_hashcrack_title():
    """
    Print centered hashCrack ASCII art logo in blue color.
    This function is used by the menu to display the program title.
    """
    terminal_width = shutil.get_terminal_size().columns
    ascii_art = [
r" ▄  █ ██      ▄▄▄▄▄    ▄  █ ▄█▄    █▄▄▄▄ ██   ▄█▄    █  █▀",
r"█   █ █ █    █     ▀▄ █   █ █▀ ▀▄  █  ▄▀ █ █  █▀ ▀▄  █▄█  ",
r"██▀▀█ █▄▄█ ▄  ▀▀▀▀▄   ██▀▀█ █   ▀  █▀▀▌  █▄▄█ █   ▀  █▀▄  ",
r"█   █ █  █  ▀▄▄▄▄▀    █   █ █▄  ▄▀ █  █  █  █ █▄  ▄▀ █  █ ",
r"   █     █               █  ▀███▀    █      █ ▀███▀    █  ",
r"  ▀     █               ▀           ▀      █          ▀   ",
r"       ▀                                  ▀               ",
"",
"For more information, visit: https://github.com/ente0/hashCrack"
    ]
    print("\n")
    for line in ascii_art:
        padding = (terminal_width - len(line)) // 2 if len(line) < terminal_width else 0
        print(colored(" " * padding + line, 'blue'))
    print("\n")

def show_menu(default_os):
    """
    Display the main menu for hashCrack with OS-specific options.
    Difficulty levels are right-aligned at the exact terminal edge.
    
    Parameters:
        default_os (str): Current operating system ('Linux' or 'Windows')
    
    Returns:
        str: User's menu selection
    """
    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width
    dash_separator = "-" * terminal_width
    
    print_hashcrack_title()
    print(colored(separator, 'cyan'))
    print(colored(f" Welcome to hashCrack! - Menu Options for {default_os}", 'cyan', attrs=['bold']))
    print(colored(separator, 'cyan'))
    
    menu_options = [
        ("Crack with Wordlist", "[EASY]", 'blue'),
        ("Crack with Association", "[MEDIUM]", 'green'),
        ("Crack with Brute-Force", "[HARD]", 'yellow'),
        ("Crack with Combinator", "[ADVANCED]", 'red'),
    ]
    
    print()
    for idx, (option_text, difficulty, diff_color) in enumerate(menu_options, 1):
        option_start = f" {colored(f'[{idx}]', 'cyan', attrs=['bold'])} {option_text}"
        
        visible_length = len(f" [{idx}] {option_text}")
        spaces = terminal_width - visible_length - len(difficulty)
        
        print(f"{option_start}{' ' * spaces}{colored(difficulty, diff_color, attrs=['bold'])}")
    
    print(colored(dash_separator, 'cyan'))
    utility_start = f" {colored('[0]', 'magenta', attrs=['bold'])} Clear Hashcat Potfile"
    utility_tag = "[UTILITY]"
    
    visible_utility_length = len(" [0] Clear Hashcat Potfile")
    utility_spaces = terminal_width - visible_utility_length - len(utility_tag)
    
    print(f"{utility_start}{' ' * utility_spaces}{colored(utility_tag, 'magenta', attrs=['bold'])}")
    
    print(colored("\n" + separator, 'magenta'))
    print(f" {colored('Press X to switch to Windows' if default_os == 'Linux' else 'Press X to switch to Linux', 'magenta', attrs=['bold'])}.")
    print(colored(separator, 'magenta'))
    
    user_option = input(colored("\nEnter option (0-4, X to switch OS, Q to quit): ", 'cyan', attrs=['bold'])).strip().lower()
    return user_option



def animate_text(text, delay):
    for i in range(len(text) + 1):
        clear_screen()
        print(text[:i], end="", flush=True)
        time.sleep(delay)

def get_package_script_path(script_name: str, os_type: str) -> Path:
    try:
        package_path = resources.files(f'hashCrack.{os_type.lower()}') / script_name
        
        if not package_path.exists():
            raise FileNotFoundError(f"Script {script_name} not found in package")
        
        return package_path
    except (ImportError, AttributeError):
        package_path = pkg_resources.resource_filename('hashCrack', f'{os_type.lower()}/{script_name}')
        
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Script {script_name} not found in package")
        
        return Path(package_path)

def handle_option(option, default_os, hash_file):
    script_map = {
        "1": "crack_wordlist.py",
        "2": "crack_rule.py",
        "3": "crack_bruteforce.py",
        "4": "crack_combo.py"
    }

    print("...", flush=True)

    if option.lower() == "q":
        print(colored("Done! Exiting...", 'yellow'))
        sys.exit(0)

    script_name = script_map.get(option)
    if not script_name:
        print(colored("Invalid option. Please try again.", 'red'))
        return

    try:
        script_type = "windows" if default_os == "Windows" else "linux"
        script_path = get_package_script_path(script_name, script_type)
        
        print(colored(f'Executing {script_path}', 'green'))
        
        python_cmd = "python3" if default_os == "Linux" else "python"
        os.system(f'{python_cmd} "{script_path}" "{hash_file}"')
    
    except FileNotFoundError as e:
        print(colored(f"Error: {e}", 'red'))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", 'red'))
    
    input("Press Enter to return to the menu...")

def execute_windows_scripts():
    windows_scripts_dir = "scripts/windows"
    if os.path.isdir(windows_scripts_dir):
        for script in os.listdir(windows_scripts_dir):
            script_path = os.path.join(windows_scripts_dir, script)
            if os.path.isfile(script_path):
                print(f"[+] Executing Windows script: {script}","green")
                os.system(f"python {script_path}")
    else:
        print(colored(f"[!] Error: Windows scripts directory not found: '{windows_scripts_dir}'", "red"))

def define_logs(session):
    home_dir = os.path.expanduser("~")
    log_dir = os.path.join(home_dir, ".hashCrack", "logs", session)
    os.makedirs(log_dir, exist_ok=True)
    original_plaintext_path = "plaintext.txt"
    plaintext_path = os.path.join(log_dir, "plaintext.txt")
    status_file_path = os.path.join(log_dir, "status.txt")
    return plaintext_path, status_file_path, log_dir

def save_logs(session, wordlist_path=None, wordlist=None, mask_path=None, mask=None, rule_path=None, rule=None, hash_file=None):
    plaintext_path, status_file_path, log_dir = define_logs(session)

    if not hash_file:
        hash_file = define_hashfile()

    with open(status_file_path, "w") as f:
        f.write(f"Session: {session}\n")

        if wordlist and wordlist_path:
            f.write(f"Wordlist: {os.path.join(wordlist_path, wordlist)}\n")
        else:
            f.write("Wordlist: N/A\n")

        if mask_path and mask:
            f.write(f"Mask File: {os.path.join(mask_path, mask)}\n")
        else:
            f.write(f"Mask: {mask if mask else 'N/A'}\n")

        if rule_path and rule:
            f.write(f"Rule: {os.path.join(rule_path, rule)}\n")
        elif rule:
            f.write(f"Rule: {rule}\n")
        else:
            f.write("Rule: N/A\n")

        if hash_file and os.path.exists(hash_file):
            try:
                with open(hash_file, "r") as hash_file_obj:
                    f.write(f"Hash: {hash_file_obj.read().strip()}\n")
            except Exception as e:
                print(f"[!] Error reading hash file: {e}")
                f.write("Hash: N/A\n")
        else:
            print("[!] Warning: Hash file not provided or doesn't exist.")
            f.write("Hash: N/A\n")

        if os.path.exists(plaintext_path):
            with open(plaintext_path, 'r') as plaintext_file:
                plaintext = plaintext_file.read().strip()
        else:
            plaintext = "N/A"

        f.write(f"Plaintext: {plaintext}\n")

    print(f"Status saved to {status_file_path}")

    if plaintext_path and os.path.exists(plaintext_path):
        with open(plaintext_path, "r") as plaintext_file:
            print(colored("\n[*] Plaintext Output:","blue"))
            print(plaintext_file.read().strip())

    print(colored("\n[*] Status File Content:","blue"))
    with open(status_file_path, "r") as status_file:
        print(status_file.read().strip())

def list_sessions(default_restorepath):
    try:
        restore_files = [f for f in os.listdir(default_restorepath) if f.endswith('.restore')]
        if restore_files:
            print(colored("[+] Available sessions:", "green"))
            for restore_file in restore_files:
                print(colored("[-]", "yellow") + f" {restore_file}")
        else:
            print(colored("[!] No restore files found...", "red"))
    except FileNotFoundError:
        print(colored(f"[!] Error: The directory {default_restorepath} does not exist.", "red"))

def restore_session(restore_file_input, default_restorepath):
    restore_file = restore_file_input.strip() or default_restorepath

    if restore_file.strip() == default_restorepath and not os.path.isfile(restore_file):
        return

    if not os.path.isabs(restore_file):
        restore_file = os.path.join(default_restorepath, restore_file)

    if not os.path.isfile(restore_file):
        print(colored(f"[!] Error: Restore file '{restore_file}' not found.", 'red'))
        return

    session = os.path.basename(restore_file).replace(".restore", "")
    print(colored(f"[+] Restoring session >> {restore_file}", 'blue'))

    cmd = f"hashcat --session={session} --restore"
    print(colored(f"[*] Executing: {cmd}", "blue"))
    os.system(cmd)


def define_hashfile():
    parser = argparse.ArgumentParser(description="A tool for cracking hashes using Hashcat.")
    parser.add_argument("hash_file", help="Path to the file containing the hash to crack")
    args = parser.parse_args()

    if not os.path.isfile(args.hash_file):
        print(colored(f"[!] Error: The file '{args.hash_file}' does not exist.", 'red'))
        time.sleep(2)
        sys.exit(1)

    if os.stat(args.hash_file).st_size == 0:
        print(colored(f"[!] Error: The file '{args.hash_file}' is empty.", 'red'))
        time.sleep(2)
        sys.exit(1)

    return args.hash_file

def clean_hashcat_cache():
    try:
        potfile_paths = [
            Path.home() / '.local/share/hashcat/hashcat.potfile',
            Path.home() / '.hashcat/hashcat.potfile',
            #Path('/root/.hashcat/hashcat.potfile'),
            #Path('/root/.local/share/hashcat/hashcat.potfile'),
            Path.home() / 'venv/lib/python3.12/site-packages/hashcat/hashcat/hashcat.potfile'
        ]
        
        for potfile in potfile_paths:
            if potfile.exists():
                potfile.unlink()
                print(colored(f"[+] Removed existing potfile: {potfile}", 'green'))
    
        return True
    except Exception as e:
        print(colored(f"[!] Error cleaning hashcat cache: {e}", 'red'))
        return False

def get_unique_session_name(session_name, log_path="~/.hashCrack/logs/"):
    expanded_path = os.path.expanduser(log_path)
    
    counter = 0
    while True:
        if counter == 0:
            unique_name = session_name
        else:
            unique_name = f"{session_name}_{counter}"
            
        full_path = os.path.join(expanded_path, unique_name)
            
        if not os.path.isdir(full_path):
            return unique_name
            
        counter += 1