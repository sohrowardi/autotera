import pyautogui
import time
import pyperclip
import os
import keyboard

pyautogui.FAILSAFE = False  # Disable the fail-safe

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)

print(f"Current working directory: {os.getcwd()}")

# Function to process and paste links from a given list of lines
def paste_links(lines):
    for i, line in enumerate(lines):
        print(f"Pasting line {i+1}: {line.strip()}")
        pyautogui.hotkey('ctrl', 'l')  # Focus on the address bar
        time.sleep(0.2)
        pyperclip.copy(line.strip())  # Copy the line to clipboard
        pyautogui.hotkey('ctrl', 'v')  # Paste the line
        time.sleep(0.2)
        pyautogui.press('enter')  # Press Enter after pasting
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 't')  # Open a new tab
        time.sleep(0.2)

# Function to process and paste links from links.txt
def process_links():
    with open('links.txt', 'r') as file:
        lines = file.readlines()

    # Perform the actions for the first 15 lines or fewer if there aren't enough lines
    lines_to_paste = lines[:15]
    paste_links(lines_to_paste)

    # Append the first 15 lines to links_archived.txt
    with open('links_archived.txt', 'a') as archived_file:
        archived_file.writelines(lines_to_paste)

    # Print the archived lines
    print("Archived the following lines:")
    for line in lines_to_paste:
        print(line.strip())

    # Remove the first 15 lines from links.txt
    with open('links.txt', 'w') as file:
        file.writelines(lines[15:])

    # Print a message indicating completion of deletion
    print("Deleted the first 15 lines from links.txt")

# Function to process and paste the last 15 links from links_archived.txt
def process_archived_links():
    with open('links_archived.txt', 'r') as file:
        lines = file.readlines()

    # Perform the actions for the last 15 lines or fewer if there aren't enough lines
    lines_to_paste = lines[-15:]
    paste_links(lines_to_paste)

    # Print a message indicating completion
    print("Pasted the last 15 lines from links_archived.txt")

# Function to modify and replace the domain of URLs in open tabs
def modify_and_replace_domain():
    # Activate the first tab
    pyautogui.hotkey('ctrl', '1')  # Switch to the first tab
    time.sleep(0.2)  # Ensure tab switch is complete
    
    for _ in range(15):  # Loop for 15 tabs
        pyautogui.hotkey('ctrl', 'l')  # Focus on the address bar
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')  # Copy the current URL
        time.sleep(0.2)

        current_url = pyperclip.paste()  # Get the copied URL
        print(f"Original URL: {current_url}")
        
        # Replace the domain with terabox.com
        modified_url = current_url.split("//")[-1].split("/", 1)
        if len(modified_url) > 1:
            modified_url = "https://terabox.com/" + modified_url[1]
        else:
            modified_url = "https://terabox.com/"

        print(f"Modified URL: {modified_url}")
        pyperclip.copy(modified_url)  # Copy the modified URL to clipboard
        pyautogui.hotkey('ctrl', 'v')  # Paste the modified URL
        pyautogui.press('enter')  # Press Enter to navigate to the modified URL
        time.sleep(0.5)  # Added a delay for the URL to load

        if _ < 14:  # Ensure the next tab switch only happens if there are more tabs
            pyautogui.hotkey('ctrl', 'pagedown')  # Move to the next tab
            time.sleep(0.5)  # Added a delay to ensure the tab switch completes

def main_loop():
    print("Press 'Space' to paste the first 15 links from 'links.txt' into open tabs.")
    print("Press '1' to paste the last 15 links from 'links_archived.txt' into open tabs.")
    print("Press '2' to modify the domain of the current URLs in open tabs to 'terabox.com' and move to the next tab.")

    while True:
        # Block until either "Space" or "1" or "2" is pressed
        if keyboard.is_pressed('1'):
            print("1 detected")
            process_archived_links()
            while keyboard.is_pressed('1'):
                time.sleep(0.1)  # Wait for key to be released
        elif keyboard.is_pressed('2'):
            print("2 detected")
            modify_and_replace_domain()
            while keyboard.is_pressed('2'):
                time.sleep(0.1)  # Wait for key to be released
        elif keyboard.is_pressed('space'):
            print("Space detected")
            process_links()
            while keyboard.is_pressed('space'):
                time.sleep(0.1)  # Wait for Space to be released

if __name__ == "__main__":
    main_loop()
