#!/usr/bin/env python3

import os
import time
import sys

# --- Configuration ---
USE_AZERTY = False  # True = AZERTY layout, False = QWERTY

# --- Keymaps ---
key_map_qwerty = {
    'A': (0x04, 0),
    'B': (0x05, 0),
    'C': (0x06, 0),
    'D': (0x07, 0),
    'E': (0x08, 0),
    'F': (0x09, 0),
    'G': (0x0A, 0),
    'H': (0x0B, 0),
    'I': (0x0C, 0),
    'J': (0x0D, 0),
    'K': (0x0E, 0),
    'L': (0x0F, 0),
    'M': (0x10, 0),
    'N': (0x11, 0),
    'O': (0x12, 0),
    'P': (0x13, 0),
    'Q': (0x14, 0),
    'R': (0x15, 0),
    'S': (0x16, 0),
    'T': (0x17, 0),
    'U': (0x18, 0),
    'V': (0x19, 0),
    'W': (0x1A, 0),
    'X': (0x1B, 0),
    'Y': (0x1C, 0),
    'Z': (0x1D, 0),
    '1': (0x1E, 0),
    '2': (0x1F, 0),
    '3': (0x20, 0),
    '4': (0x21, 0),
    '5': (0x22, 0),
    '6': (0x23, 0),
    '7': (0x24, 0),
    '8': (0x25, 0),
    '9': (0x26, 0),
    '0': (0x27, 0),
    'ENTER': (0x28, 0),
    'ESCAPE': (0x29, 0),
    'BACKSPACE': (0x2A, 0),
    'TAB': (0x2B, 0),
    'SPACE': (0x2C, 0),
    'MINUS': (0x2D, 0),
    'EQUAL': (0x2E, 0),
    'LEFTBRACE': (0x2F, 0),
    'RIGHTBRACE': (0x30, 0),
    'BACKSLASH': (0x31, 0),
    'SEMICOLON': (0x33, 0),
    'APOSTROPHE': (0x34, 0),
    'GRAVE': (0x35, 0),
    'COMMA': (0x36, 0),
    'DOT': (0x37, 0),
    'SLASH': (0x38, 0),
    'CAPSLOCK': (0x39, 0),
    'F1': (0x3A, 0),
    'F2': (0x3B, 0),
    'F3': (0x3C, 0),
    'F4': (0x3D, 0),
    'F5': (0x3E, 0),
    'F6': (0x3F, 0),
    'F7': (0x40, 0),
    'F8': (0x41, 0),
    'F9': (0x42, 0),
    'F10': (0x43, 0),
    'F11': (0x44, 0),
    'F12': (0x45, 0),
    'RIGHTARROW': (0x4F, 0),
    'LEFTARROW': (0x50, 0),
    'DOWNARROW': (0x51, 0),
    'UPARROW': (0x52, 0),
}

key_map_azerty = {**key_map_qwerty}
key_map = key_map_azerty if USE_AZERTY else key_map_qwerty

# Modifier constants
MOD_LCTRL = 0x01
MOD_LSHIFT = 0x02
MOD_LALT = 0x04
MOD_LGUI = 0x08

# --- Functions ---
def send_key(hidg, keycode, modifier=0, delay=0.05):
    report = bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00])
    os.write(hidg, report)
    time.sleep(delay)
    report = bytes([0] * 8)
    os.write(hidg, report)
    time.sleep(delay)

def send_string(hidg, string, key_map):
    for char in string:
        if char == ' ':
            send_key(hidg, key_map['SPACE'][0])
            continue
        upper = char.isupper()
        char = char.upper()
        if char in key_map:
            keycode, mod = key_map[char]
            if upper:
                send_key(hidg, keycode, modifier=MOD_LSHIFT)
            else:
                send_key(hidg, keycode)
        else:
            print(f"[!] Unknown character: '{char}'")

def send_combo(hidg, keys, key_map):
    modifier = 0
    keycodes = []

    for key in keys:
        if key == 'CTRL':
            modifier |= MOD_LCTRL
        elif key == 'SHIFT':
            modifier |= MOD_LSHIFT
        elif key == 'ALT':
            modifier |= MOD_LALT
        elif key == 'GUI':
            modifier |= MOD_LGUI
        else:
            key = key.upper()
            if key in key_map:
                keycodes.append(key_map[key][0])

    # Only sending first keycode for simplicity
    if keycodes:
        send_key(hidg, keycodes[0], modifier)

def send_file_as_string(hidg, filepath, key_map):
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()

    send_string(hidg, content, key_map)

# --- DuckyScript Parser ---
def parse_duckyscript(filepath, hidg, key_map):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('//'):
            continue

        parts = line.split(' ', 1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ''

        if command == 'DELAY':
            ms = int(args)
            print(f"[i] Delay {ms}ms")
            time.sleep(ms / 1000.0)

        elif command == 'STRING':
            print(f"[i] Typing '{args}'")
            send_string(hidg, args, key_map)

        elif command in ['ENTER', 'TAB', 'ESCAPE', 'BACKSPACE', 'UPARROW', 'DOWNARROW', 'LEFTARROW', 'RIGHTARROW', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']:
            print(f"[i] Pressing {command}")
            send_key(hidg, key_map[command][0])

        elif command == 'REM':
            print(f"[i] Comment: {args}")

        elif command == 'COMBO':
            keys = args.split(' ')
            send_combo(hidg, keys, key_map)

        elif command == 'TYPEFILE':
            print(f"[i] Typing file contents from {args}")
            send_file_as_string(hidg, args, key_map)

        else:
            print(f"[!] Unknown command: {command}")

# --- Main ---
def main():
    if len(sys.argv) != 2:
        print(f"Usage: sudo python3 {sys.argv[0]} <payload.txt>")
        exit(1)

    hidg = os.open("/dev/hidg0", os.O_RDWR | os.O_NONBLOCK)
    payload_file = sys.argv[1]

    parse_duckyscript(payload_file, hidg, key_map)

    os.close(hidg)

if __name__ == "__main__":
    main()
