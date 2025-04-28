# Airgapped Stealth RCE

## Introduction

This tool is designed for red teaming in offensive security. It involves modifying a real Human Interface Device (HID), such as a keyboard, by embedding a small microprocessor (e.g., Raspberry Pi) and a cellular modem (e.g., LTE/5G module) for data extraction and remote control. This method differs from existing methods like NSA TAO COTTONMOUTH and Hak5 RubberDucky. Using an airgapped network like LTE bypasses all established network-related security measures, such as Intrusion Detection Systems (IDS), Intrusion Prevention Systems (IPS), and firewalls. Encrypting LTE traffic and enabling remote module updates makes it a very stealthy tool.

## Key Features
- **Stealth Integration**: The device appears as a regular, functioning keyboard to the target.
- **Autonomous Operation**: Communication happens via LTE/5G without touching the target’s network stack.
- **Encrypted Traffic**: The LTE connection can be fully encrypted, adding an extra layer of stealth.
- **Remote Reconfiguration**: The device can be updated remotely after deployment via cellular commands.
- **Increased Capability**: Unlike basic HID attacks, the microprocessor can perform complex operations, such as post-exploitation frameworks, tunneling, or custom backdoors.

## Advantages Over Traditional Methods
- **Bypass Network Defenses**: It bypasses firewalls, IDS, and IPS.
- **Persistent Access**: It maintains access even if the network is monitored or restricted.
- **Difficult to Detect**: It's challenging to detect without physical hardware inspection.

## Threat Model
This device targets environments with strong network defenses where traditional methods are ineffective. The attack assumes:
- **Physical Access**: Initial short-term access to install or replace a peripheral device.
- **Limited Inspection**: Hardware devices like keyboards are trusted and rarely inspected.
- **Network Isolation**: The target machine may be isolated from the internet, making traditional remote access tools ineffective.
- **Assumed Trust**: HID devices are automatically trusted by operating systems without extensive verification.

## Deployment Strategy

### Preparation:
1. Modify a commercial keyboard to embed a microprocessor (e.g., Raspberry Pi) and LTE/5G modem module.
2. Preload software: reverse shell clients, command-and-control scripts, LTE encryption modules.

### Physical Insertion:
- Replace the target's keyboard with the modified one during a physical access window (e.g., insider threat, supply chain attack, or physical red team operation).

### Activation and Persistence:
- The device operates independently using its LTE connection, receiving commands, exfiltrating data, or executing payloads.

### Remote Operation:
- Operators can remotely send encrypted signals over the mobile network to control the device.

## Detection & Mitigations

Although detection is difficult, possible defensive measures include:
- **Hardware Inspections**: Regular visual inspections to detect tampering.
- **Peripheral Whitelisting**: Allow only approved devices (based on USB device IDs and serial numbers).
- **USB Monitoring Software**: Detect anomalous USB behaviors.
- **Physical Security Measures**: Secure physical access and conduct supply chain checks.
- **RF Monitoring**: Detect unexpected LTE/5G transmissions inside secure facilities.

## Use Cases
- **Penetration Testing**: Simulate APTs that use hardware implants to bypass traditional security.
- **Supply Chain Attacks**: Demonstrate risks when peripherals are compromised during manufacturing or shipping.
- **Red Team Operations**: Deploy in engagements where network access is restricted, but physical access is possible.
- **Covert Persistence**: Maintain long-term, low-noise access to high-value targets.

## Proof of Concept - Demo

### Materials Used:
- Logitech G512 gaming keyboard
- Raspberry Pi 4b (4GB RAM)

### Steps:

#### 1. Disassemble the Keyboard
- Remove screws and keycaps, open the keyboard case.

#### 2. Setup Raspberry Pi OS
- Install Raspberry Pi OS 64-bit with SSH access for setup.

#### 3. Configure Raspberry Pi to Act as an HID Device

**⚠️ Important!** For each code files, just copy and paste the contents in the directories for the most updated code!

Edit `/boot/config.txt`:
```bash
sudo nano /boot/config.txt
```
Add:
```bash
dtoverlay=dwc2
```

Edit `/boot/cmdline.txt`:
```bash
sudo nano /boot/cmdline.txt
```
Add `modules-load=dwc2,g_hid` just after `rootwait`.

#### 4. Setup HID Gadget Script

Create the file `/usr/bin/keyboard-gadget.sh`:
```bash
sudo nano /usr/bin/keyboard-gadget.sh
```

Add the following content to make the Raspberry Pi act as a USB keyboard:
/usr/bin/keyboard-gadget.sh

#### 5. Create Systemd Service for HID Gadget

Create a new systemd service to make the keyboard gadget auto-start on boot:
```bash
sudo nano /etc/systemd/system/keyboard-gadget.service
```
Add:
/etc/systemd/system/keyboard-gadget.service

Reload the systemd service and enable it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable keyboard-gadget.service
sudo systemctl start keyboard-gadget.service
```

#### 6. Running macroscript
```bash
sudo nano /home/your_username
```
Add:
/home/username/macroscript_runner.py
