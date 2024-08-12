import pyautogui
import time
import pyperclip

pyautogui.FAILSAFE = False  # Disable the fail-safe

# Give 3 seconds to prepare
time.sleep(3)

# Open the text file and read lines
with open('text.txt', 'r') as file:
    lines = file.readlines()

# Perform the actions for the first 15 lines
for i in range(15):
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.2)  # Adding a small delay
    pyperclip.copy(lines[i].strip())  # Copy the line to clipboard
    pyautogui.hotkey('ctrl', 'v')  # Paste the line
    time.sleep(0.3)  # Adding a small delay
    pyautogui.press('enter')  # Press Enter after pasting
    time.sleep(0.2)  # Adding a small delay
    pyautogui.hotkey('ctrl', 't')
    time.sleep(0.2)  # Adding a small delay

# Remove the first 15 lines from the file
with open('text.txt', 'w') as file:
    file.writelines(lines[15:])
