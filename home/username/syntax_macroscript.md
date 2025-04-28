# DuckyScript Supported Syntax (duckyscript_runner.py)

## Basic Commands

| Command       | Description                                |
|---------------|--------------------------------------------|
| `DELAY <ms>`  | Waits for `<ms>` milliseconds              |
| `STRING <text>` | Types the text as keystrokes             |
| `ENTER`       | Presses the Enter key                     |
| `TAB`         | Presses the Tab key                       |
| `ESCAPE`      | Presses the Escape key                    |
| `BACKSPACE`   | Presses the Backspace key                  |
| `UPARROW`     | Presses the Up arrow key                   |
| `DOWNARROW`   | Presses the Down arrow key                 |
| `LEFTARROW`   | Presses the Left arrow key                 |
| `RIGHTARROW`  | Presses the Right arrow key                |
| `REM <comment>` | Adds a comment (ignored by parser)      |

## Combination Keys

| Command         | Description                                             |
|-----------------|---------------------------------------------------------|
| `COMBO CTRL ALT DELETE` | Sends CTRL+ALT+DEL combination                  |
| `COMBO CTRL A`          | Sends CTRL+A (Select all)                       |
| `COMBO GUI R`           | Sends Windows key + R (Run prompt on Windows)   |
| `COMBO SHIFT TAB`       | Sends SHIFT+TAB                                 |

## File Transfer via Keyboard (HID Exfiltration)

| Command           | Description                                                |
|-------------------|------------------------------------------------------------|
| `TYPEFILE <path>` | Types the content of the file character by character        |

Example payload:

```plaintext
REM Start of script
DELAY 1000
COMBO GUI
STRING Word
ENTER
DELAY 500
COMBO CTRL ALT DELETE
DELAY 500
