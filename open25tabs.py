import pyautogui
import time
import pyperclip
import keyboard  # Import the keyboard module

pyautogui.FAILSAFE = False  # Disable the fail-safe

# Function to process and paste links
def process_links():
    with open('links.txt', 'r') as file:
        lines = file.readlines()

    # Perform the actions for the first 15 lines or fewer if there aren't enough lines
    for i in range(min(15, len(lines))):
        print(f"Pasting line {i+1}: {lines[i].strip()}")
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.2)  # Adding a small delay
        pyperclip.copy(lines[i].strip())  # Copy the line to clipboard
        pyautogui.hotkey('ctrl', 'v')  # Paste the line
        time.sleep(0.3)  # Adding a small delay
        pyautogui.press('enter')  # Press Enter after pasting
        time.sleep(0.2)  # Adding a small delay
        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.2)  # Adding a small delay

    # Append the first 15 lines to links_archived.txt
    with open('links_archived.txt', 'a') as archived_file:
        archived_file.writelines(lines[:15])

    # Print the archived lines
    print("Archived the following lines:")
    for line in lines[:15]:
        print(line.strip())

    # Remove the first 15 lines from links.txt
    with open('links.txt', 'w') as file:
        file.writelines(lines[15:])

    # Print a message indicating completion of deletion
    print("Deleted the first 15 lines from links.txt")

def main_loop():
    while True:
        # Wait for the user to press "Enter" anywhere on the system
        print("Waiting for 'Enter' key press...")
        keyboard.wait('enter')

        # Process the first 15 links
        process_links()

        # Check if the user wants to exit
        user_input = input('Press "Enter" to continue or type "exit" to stop: ')
        if user_input.lower() == 'exit':
            print("Exiting the program...")
            break

if __name__ == "__main__":
    main_loop()
