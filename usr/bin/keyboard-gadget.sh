#!/bin/bash
set -e

modprobe libcomposite

GADGET_DIR=/sys/kernel/config/usb_gadget/keyboard
mkdir -p $GADGET_DIR
cd $GADGET_DIR

echo 0x046d > idVendor  # Logitech
echo 0xc31c > idProduct # Keyboard
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB

mkdir -p strings/0x409
echo "deadbeef12345678" > strings/0x409/serialnumber
echo "Raspberry Pi" > strings/0x409/manufacturer
echo "Pi HID Keyboard" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Config 1: HID Keyboard" > configs/c.1/strings/0x409/configuration
echo 120 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

# HID Report Descriptor for keyboard
echo -ne '\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x01\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0' > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/

# Setup UDC
UDC=$(ls /sys/class/udc | head -n 1)
echo "$UDC" > UDC
