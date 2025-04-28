# Duckyscript Syntax - Raspberry Pi HID Runner

## Basic Commands

| Command | Description                          | Example                        |
|---------|--------------------------------------|--------------------------------|
| REM     | Comment line (ignored)               | REM This is a comment          |
| STRING  | Types out a text string               | STRING Hello, World!           |
| ENTER   | Presses the Enter key                 | ENTER                          |
| DELAY   | Waits X milliseconds                  | DELAY 1000                     |
| GUI     | Presses Windows key + optional letter | GUI r                         |
| CTRL    | Presses Control key + letter          | CTRL c                         |
| ALT     | Presses Alt key + letter              | ALT f                          |
| SHIFT   | Presses Shift key + letter            | SHIFT a                        |

## Special Notes
- `GUI` without argument presses only the Windows key (to open Windows Search).
- Uppercase letters automatically send `SHIFT`.
- Timing can be adjusted using `DELAY`.

## Example Script

```plaintext
REM Launch Notepad
GUI
DELAY 500
STRING notepad
ENTER
DELAY 1000
STRING Hello World!
ENTER
