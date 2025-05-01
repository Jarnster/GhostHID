#!/usr/bin/env python3

import os
import sys
import time

# === CONFIGURATION ===
USE_AZERTY = False  # Will be overwritten if provided via CLI

# === HID MODIFIER BITS ===
MOD_NONE = 0x00
MOD_LCTRL = 0x01
MOD_LSHIFT = 0x02
MOD_LALT = 0x04
MOD_LGUI = 0x08  # Windows key
MOD_RCTRL = 0x10
MOD_RSHIFT = 0x20
MOD_RALT = 0x40
MOD_RGUI = 0x80

# === KEYMAPS ===
key_map_qwerty = {
    'A': 0x04, 'B': 0x05, 'C': 0x06, 'D': 0x07,
    'E': 0x08, 'F': 0x09, 'G': 0x0A, 'H': 0x0B,
    'I': 0x0C, 'J': 0x0D, 'K': 0x0E, 'L': 0x0F,
    'M': 0x10, 'N': 0x11, 'O': 0x12, 'P': 0x13,
    'Q': 0x14, 'R': 0x15, 'S': 0x16, 'T': 0x17,
    'U': 0x18, 'V': 0x19, 'W': 0x1A, 'X': 0x1B,
    'Y': 0x1C, 'Z': 0x1D,
    '1': 0x1E, '2': 0x1F, '3': 0x20, '4': 0x21,
    '5': 0x22, '6': 0x23, '7': 0x24, '8': 0x25,
    '9': 0x26, '0': 0x27,
    'ENTER': 0x28,
    'ESC': 0x29,
    'BACKSPACE': 0x2A,
    'TAB': 0x2B,
    'SPACE': 0x2C,
    'MINUS': 0x2D,
    'EQUAL': 0x2E,
    'LEFTBRACE': 0x2F,
    'RIGHTBRACE': 0x30,
    'SEMICOLON': 0x33,
    'APOSTROPHE': 0x34,
    'GRAVE': 0x35,
    'COMMA': 0x36,
    'DOT': 0x37,
    'SLASH': 0x38,
    'CAPSLOCK': 0x39,
}

key_map_azerty = {
    'A': 0x14,  # Q on QWERTY (A on AZERTY is where Q is on QWERTY)
    'B': 0x05,  # B stays same
    'C': 0x06,  # C stays same
    'D': 0x07,  # D stays same
    'E': 0x08,  # E stays same
    'F': 0x09,  # F stays same
    'G': 0x0A,  # G stays same
    'H': 0x0B,  # H stays same
    'I': 0x0C,  # I stays same
    'J': 0x0D,  # J stays same
    'K': 0x0E,  # K stays same
    'L': 0x0F,  # L stays same
    'M': 0x33,  # on QWERTY (M on AZERTY is where ; is on QWERTY)
    'N': 0x11,  # N stays same
    'O': 0x12,  # O stays same
    'P': 0x13,  # P stays same
    'Q': 0x1A,  # A on QWERTY (Q on AZERTY is where A is on QWERTY)
    'R': 0x15,  # R stays same
    'S': 0x16,  # S stays same
    'T': 0x17,  # T stays same
    'U': 0x18,  # U stays same
    'V': 0x19,  # V stays same
    'W': 0x1D,  # Z on QWERTY (W on AZERTY is where Z is on QWERTY)
    'X': 0x1B,  # X stays same
    'Y': 0x1C,  # Y stays same (but position is different)
    'Z': 0x1A,  # W on QWERTY (Z on AZERTY is where W is on QWERTY)

    # Numbers (first row)
    '1': 0x1E,  # 1 stays same
    '2': 0x1F,  # 2 stays same
    '3': 0x20,  # 3 stays same
    '4': 0x21,  # 4 stays same
    '5': 0x22,  # 5 stays same
    '6': 0x23,  # 6 is actually & on AZERTY but same keycode
    '7': 0x24,  # 7 is actually é on AZERTY but same keycode
    '8': 0x25,  # 8 is actually " on AZERTY but same keycode
    '9': 0x26,  # 9 is actually ( on AZERTY but same keycode
    '0': 0x27,  # 0 is actually à on AZERTY but same keycode

    # Special characters
    'MINUS': 0x2D,    # ) on AZERTY
    'EQUAL': 0x2E,    # = on AZERTY (but shifted to +)
    'LEFTBRACE': 0x2F,  # ^ on AZERTY
    'RIGHTBRACE': 0x30, # $ on AZERTY
    'SEMICOLON': 0x34,  # M on AZERTY is where ; is on QWERTY
    'APOSTROPHE': 0x33, # ù on AZERTY
    'GRAVE': 0x35,      # ! on AZERTY
    'COMMA': 0x36,      # ; on AZERTY
    'DOT': 0x37,        # : on AZERTY
    'SLASH': 0x38,      # = on AZERTY

    # Function keys
    'ENTER': 0x28,
    'ESC': 0x29,
    'BACKSPACE': 0x2A,
    'TAB': 0x2B,
    'SPACE': 0x2C,
    'CAPSLOCK': 0x39,
}

def get_key_code(char):
    upper_char = char.upper()
    if USE_AZERTY:
        # Special cases for AZERTY lowercase letters that need different keycodes
        lower_to_upper = {
            'a': 'Q',
            'q': 'A',
            'w': 'Z',
            'z': 'W',
            'm': 'SEMICOLON',
            ',': 'SEMICOLON',
            ';': 'COMMA',
            ':': 'DOT',
            '!': 'GRAVE',
            'é': '7',
            '"': '8',
            "'": 'APOSTROPHE',
            'à': '0',
            ')': 'MINUS',
            '=': 'EQUAL',
            '^': 'LEFTBRACE',
            '$': 'RIGHTBRACE',
            'ù': 'APOSTROPHE',
            'µ': 'RIGHTBRACE'  # Might need adjustment
        }
        if char.islower() and char in lower_to_upper:
            upper_char = lower_to_upper[char]
    
    if upper_char in key_map:
        return key_map[upper_char]
    return None
key_map = key_map_azerty if USE_AZERTY else key_map_qwerty

# === FUNCTIONS ===

def open_hid_device():
    try:
        return os.open("/dev/hidg0", os.O_RDWR)
    except Exception as e:
        print(f"[x] Failed to open HID device: {e}")
        sys.exit(1)

def send_key(hidg, hid_code, modifier=MOD_NONE):
    report = bytes([modifier, 0x00, hid_code, 0x00, 0x00, 0x00, 0x00, 0x00])
    os.write(hidg, report)
    time.sleep(0.005)
    os.write(hidg, bytes(8))  # Release all keys
    time.sleep(0.005)

def type_text(hidg, text):
    for char in text:
        upper = char.isupper()
        char = char.upper()
        if char in key_map:
            code = key_map[char]
            mod = MOD_LSHIFT if upper else MOD_NONE
            print(f"[+] Typing '{char}' (code={hex(code)}, modifier={hex(mod)})")
            send_key(hidg, code, mod)
        elif char == ' ':
            print("[+] Typing SPACE")
            send_key(hidg, key_map['SPACE'], MOD_NONE)
        else:
            print(f"[!] Unknown character '{char}'")

def run_payload_script(hidg, file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[x] Error reading file {file_path}: {e}")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if not line or line.startswith("//"):
            continue  # Comment or empty line

        print(f"[>] Executing: {line}")
        parts = line.split(' ', 1)
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else ''

        if cmd == "STRING":
            type_text(hidg, arg)
        elif cmd == "DELAY":
            delay_time = int(arg) / 1000
            print(f"[+] Delay for {delay_time} seconds")
            time.sleep(delay_time)
        elif cmd == "ENTER":
            print("[+] Pressing ENTER")
            send_key(hidg, key_map['ENTER'])
        elif cmd == "GUI":
            if arg:
                print(f"[+] GUI + {arg}")
                send_combo(hidg, key_map[arg.upper()], MOD_LGUI)
            else:
                print("[+] Pressing Windows key alone")
                send_key(hidg, 0x00, MOD_LGUI)
        elif cmd == "ALT":
            print(f"[+] ALT + {arg}")
            send_combo(hidg, key_map[arg.upper()], MOD_LALT)
        elif cmd == "CTRL":
            print(f"[+] CTRL + {arg}")
            send_combo(hidg, key_map[arg.upper()], MOD_LCTRL)
        else:
            print(f"[!] Unknown command '{cmd}'")

def send_combo(hidg, hid_code, modifier):
    report = bytes([modifier, 0x00, hid_code, 0x00, 0x00, 0x00, 0x00, 0x00])
    os.write(hidg, report)
    time.sleep(0.05)
    os.write(hidg, bytes(8))
    time.sleep(0.05)

def main():
    global USE_AZERTY, key_map

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <payload_file> [azerty]")
        sys.exit(1)

    file_path = sys.argv[1]

    if len(sys.argv) >= 3:
        layout = sys.argv[2].lower()
        if layout == "azerty":
            USE_AZERTY = True
            print("[+] Using AZERTY keymap")
        else:
            print("[+] Using QWERTY keymap")

    key_map = key_map_azerty if USE_AZERTY else key_map_qwerty

    hidg = open_hid_device()
    run_payload_script(hidg, file_path)
    os.close(hidg)

if __name__ == "__main__":
    main()
