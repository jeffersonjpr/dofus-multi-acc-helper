import keyboard
import pyautogui
import time
import pygetwindow as gw
import re

MAIN_DELAY = 0.3

# Press 'Alt' key before the loop starts
pyautogui.press('altleft')

dofus_version = re.compile(r".*Dofus (^\d+(\.\d+)*)*")

dofus_windows = [win for win in gw.getAllTitles() if dofus_version.match(win)]

print("Dofus windows found:")
for window in dofus_windows:
    print(window)


def activate_window(window_name):
    try:
        window = gw.getWindowsWithTitle(window_name)[0]
        window.activate()
        while not window.isActive:
            time.sleep(0.1)
        return
    except Exception as e:
        print(f"Error activating window: {e}")
    print(f"Window not found: {window_name}")


def repeat_mouse_click(window_names):
    mouse_position = pyautogui.position()
    for window_name in window_names:
        activate_window(window_name)
        time.sleep(MAIN_DELAY)
        pyautogui.click(mouse_position[0], mouse_position[1])


def main():
    while True:
        if keyboard.is_pressed('f5'):
            while keyboard.is_pressed('f5'):  # wait for key release
                time.sleep(0.1)
            repeat_mouse_click(dofus_windows)


if __name__ == "__main__":
    main()
