#!/usr/bin/env python3

import evdev
import os

# Constant to switch between AZERTY and QWERTY layouts
USE_AZERTY = False  # Set to True for AZERTY, False for QWERTY

# HID modifier bits
MOD_NONE = 0x00
MOD_LSHIFT = 0x02

# HID mapping (QWERTY layout by default)
key_map_qwerty = {
    'KEY_A': (0x04, MOD_NONE),
    'KEY_B': (0x05, MOD_NONE),
    'KEY_C': (0x06, MOD_NONE),
    'KEY_D': (0x07, MOD_NONE),
    'KEY_E': (0x08, MOD_NONE),
    'KEY_F': (0x09, MOD_NONE),
    'KEY_G': (0x0A, MOD_NONE),
    'KEY_H': (0x0B, MOD_NONE),
    'KEY_I': (0x0C, MOD_NONE),
    'KEY_J': (0x0D, MOD_NONE),
    'KEY_K': (0x0E, MOD_NONE),
    'KEY_L': (0x0F, MOD_NONE),
    'KEY_M': (0x10, MOD_NONE),
    'KEY_N': (0x11, MOD_NONE),
    'KEY_O': (0x12, MOD_NONE),
    'KEY_P': (0x13, MOD_NONE),
    'KEY_Q': (0x14, MOD_NONE),
    'KEY_R': (0x15, MOD_NONE),
    'KEY_S': (0x16, MOD_NONE),
    'KEY_T': (0x17, MOD_NONE),
    'KEY_U': (0x18, MOD_NONE),
    'KEY_V': (0x19, MOD_NONE),
    'KEY_W': (0x1A, MOD_NONE),
    'KEY_X': (0x1B, MOD_NONE),
    'KEY_Y': (0x1C, MOD_NONE),
    'KEY_Z': (0x1D, MOD_NONE),
    'KEY_1': (0x1E, MOD_NONE),
    'KEY_2': (0x1F, MOD_NONE),
    'KEY_3': (0x20, MOD_NONE),
    'KEY_4': (0x21, MOD_NONE),
    'KEY_5': (0x22, MOD_NONE),
    'KEY_6': (0x23, MOD_NONE),
    'KEY_7': (0x24, MOD_NONE),
    'KEY_8': (0x25, MOD_NONE),
    'KEY_9': (0x26, MOD_NONE),
    'KEY_0': (0x27, MOD_NONE),
    'KEY_ENTER': (0x28, MOD_NONE),
    'KEY_ESC': (0x29, MOD_NONE),
    'KEY_BACKSPACE': (0x2A, MOD_NONE),
    'KEY_TAB': (0x2B, MOD_NONE),
    'KEY_SPACE': (0x2C, MOD_NONE),
    'KEY_MINUS': (0x2D, MOD_NONE),
    'KEY_EQUAL': (0x2E, MOD_NONE),
    'KEY_LEFTBRACE': (0x2F, MOD_NONE),
    'KEY_RIGHTBRACE': (0x30, MOD_NONE),
    'KEY_SEMICOLON': (0x33, MOD_NONE),
    'KEY_APOSTROPHE': (0x34, MOD_NONE),
    'KEY_GRAVE': (0x35, MOD_NONE),
    'KEY_COMMA': (0x36, MOD_NONE),
    'KEY_DOT': (0x37, MOD_NONE),
    'KEY_SLASH': (0x38, MOD_NONE),
    'KEY_LEFTSHIFT': (0x00, MOD_LSHIFT),
    'KEY_RIGHTSHIFT': (0x00, MOD_LSHIFT),
    'KEY_LEFTCTRL': (0x00, 0x01),
    'KEY_RIGHTCTRL': (0x00, 0x10),
    'KEY_LEFTALT': (0x00, 0x04),
    'KEY_RIGHTALT': (0x00, 0x40),
    'KEY_LEFTMETA': (0x00, 0x08),
    'KEY_RIGHTMETA': (0x00, 0x80),
}

# HID mapping (AZERTY layout)
key_map_azerty = {
    'KEY_A': (0x04, MOD_NONE),
    'KEY_B': (0x05, MOD_NONE),
    'KEY_C': (0x06, MOD_NONE),
    'KEY_D': (0x07, MOD_NONE),
    'KEY_E': (0x08, MOD_NONE),
    'KEY_F': (0x09, MOD_NONE),
    'KEY_G': (0x0A, MOD_NONE),
    'KEY_H': (0x0B, MOD_NONE),
    'KEY_I': (0x0C, MOD_NONE),
    'KEY_J': (0x0D, MOD_NONE),
    'KEY_K': (0x0E, MOD_NONE),
    'KEY_L': (0x0F, MOD_NONE),
    'KEY_M': (0x10, MOD_NONE),
    'KEY_N': (0x11, MOD_NONE),
    'KEY_O': (0x12, MOD_NONE),
    'KEY_P': (0x13, MOD_NONE),
    'KEY_Q': (0x14, MOD_NONE),
    'KEY_R': (0x15, MOD_NONE),
    'KEY_S': (0x16, MOD_NONE),
    'KEY_T': (0x17, MOD_NONE),
    'KEY_U': (0x18, MOD_NONE),
    'KEY_V': (0x19, MOD_NONE),
    'KEY_W': (0x1A, MOD_NONE),
    'KEY_X': (0x1B, MOD_NONE),
    'KEY_Y': (0x1C, MOD_NONE),
    'KEY_Z': (0x1D, MOD_NONE),
    'KEY_1': (0x1E, MOD_NONE),
    'KEY_2': (0x1F, MOD_NONE),
    'KEY_3': (0x20, MOD_NONE),
    'KEY_4': (0x21, MOD_NONE),
    'KEY_5': (0x22, MOD_NONE),
    'KEY_6': (0x23, MOD_NONE),
    'KEY_7': (0x24, MOD_NONE),
    'KEY_8': (0x25, MOD_NONE),
    'KEY_9': (0x26, MOD_NONE),
    'KEY_0': (0x27, MOD_NONE),
    'KEY_ENTER': (0x28, MOD_NONE),
    'KEY_ESC': (0x29, MOD_NONE),
    'KEY_BACKSPACE': (0x2A, MOD_NONE),
    'KEY_TAB': (0x2B, MOD_NONE),
    'KEY_SPACE': (0x2C, MOD_NONE),
    'KEY_MINUS': (0x2D, MOD_NONE),
    'KEY_EQUAL': (0x2E, MOD_NONE),
    'KEY_LEFTBRACE': (0x2F, MOD_NONE),
    'KEY_RIGHTBRACE': (0x30, MOD_NONE),
    'KEY_SEMICOLON': (0x33, MOD_NONE),
    'KEY_APOSTROPHE': (0x34, MOD_NONE),
    'KEY_GRAVE': (0x35, MOD_NONE),
    'KEY_COMMA': (0x36, MOD_NONE),
    'KEY_DOT': (0x37, MOD_NONE),
    'KEY_SLASH': (0x38, MOD_NONE),
    'KEY_LEFTSHIFT': (0x00, MOD_LSHIFT),
    'KEY_RIGHTSHIFT': (0x00, MOD_LSHIFT),
    'KEY_LEFTCTRL': (0x00, 0x01),
    'KEY_RIGHTCTRL': (0x00, 0x10),
    'KEY_LEFTALT': (0x00, 0x04),
    'KEY_RIGHTALT': (0x00, 0x40),
    'KEY_LEFTMETA': (0x00, 0x08),
    'KEY_RIGHTMETA': (0x00, 0x80),
}

# List of substrings to identify keyboard devices
keyboard_keywords = ['Keyboard', 'keyboard', 'Logitech', 'logitech', 'LOGITECH', 'RGB', 'GAMING', 'Gaming', 'PRO', 'pro', 'Pro']

# Choose the appropriate key map based on the layout constant
key_map = key_map_azerty if USE_AZERTY else key_map_qwerty

# Search for the first keyboard device
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
keyboard = None
for device in devices:
    if any(keyword in device.name for keyword in keyboard_keywords):
        keyboard = device
        break

if keyboard is None:
    print("No keyboard found..")
    exit(1)

print(f"Using keyboard: {keyboard.name} ({keyboard.path})")

# Open HID device
hidg = os.open("/dev/hidg0", os.O_RDWR | os.O_NONBLOCK)

current_modifiers = 0

# Event loop to read keyboard inputs
for event in keyboard.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        keyevent = evdev.categorize(event)
        keycode_name = keyevent.keycode
        print(f"Key pressed: {keycode_name}")
        if isinstance(keycode_name, list):
            keycode_name = keycode_name[0]  # Sometimes a list

        if keycode_name in key_map:
            hid_keycode, modifier = key_map[keycode_name]
            if keyevent.keystate == evdev.events.KeyEvent.key_down:
                if modifier:
                    current_modifiers |= modifier
                report = bytes([
                    current_modifiers,
                    0x00,
                    hid_keycode,
                    0x00, 0x00, 0x00, 0x00, 0x00
                ])
                os.write(hidg, report)
            elif keyevent.keystate == evdev.events.KeyEvent.key_up:
                if modifier:
                    current_modifiers &= ~modifier
                # Key release (only update modifiers)
                report = bytes([
                    current_modifiers,
                    0x00,
                    0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00
                ])
                os.write(hidg, report)

