import keyboard
import pyautogui
import time
import pygetwindow as gw
import re

MAIN_DELAY = 0.1

# Press 'Alt' key before the loop starts
pyautogui.press('altleft')

dofus_version = re.compile(r".*Dofus (^\d+(\.\d+)*)*")

dofus_windows = [win for win in gw.getAllTitles() if dofus_version.match(win)]

# Battle order
dofus_queue = []
current_index = 9
end_turn_button = (1387, 956)

def define_queue():
    global dofus_queue
    for window in dofus_windows:
        print(f"What is the order of {window} in the queue:")
        order = input()
        dofus_queue.append((window, int(order)))
    print("Queue defined")

    dofus_queue = sorted(dofus_queue, key=lambda x: x[1])
    for window in dofus_queue:
        print(window)

def save_queue():
    with open("queue.txt", "w") as file:
        for window in dofus_queue:
            file.write(f"{window[0]} {window[1]}\n")

def load_queue():
    global dofus_queue
    try:
        with open("queue.txt", "r") as file:
            for line in file:
                window, order = line.split('|')
                window = window.strip()
                order = order.strip()
                dofus_queue.append((window, int(order)))
    except Exception as e:
        print(f"Error loading queue: {e}")
        return
    print("Queue loaded")
    dofus_queue = sorted(dofus_queue, key=lambda x: x[1])
    for window in dofus_queue:
        print(window)

def get_next_queue():
    global current_index
    global dofus_queue
    current_index = (current_index + 1) % len(dofus_queue)
    return dofus_queue[current_index][0]

def end_turn_and_next():
    global current_index
    global end_turn_button
    if current_index == 9:
        activate_window(dofus_queue[0][0])
        current_index = 0
    else:
        click_on_position(end_turn_button, 2)
        activate_window(get_next_queue())

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


def repeat_click_all_windows(window_names, number_of_clicks=1, delay = MAIN_DELAY):
    mouse_position = pyautogui.position()
    for window_name in window_names:
        activate_window(window_name)
        click_on_position(mouse_position, number_of_clicks, delay)

def click_on_position(mouse_position, number_of_clicks, delay = MAIN_DELAY):
    for i in range(number_of_clicks):
        pyautogui.click(mouse_position)
    time.sleep(delay)

def main():
    global current_index
    queue_setup()
    print("Press F5 to click all windows once")
    print("Press F6 to click all windows twice")
    print("Press F2 to end turn and go to the next window")
    print("Press F8 to reset the queue")
    while True:
        if keyboard.is_pressed('f5'):
            while keyboard.is_pressed('f5'):  # wait for key release
                time.sleep(0.1)
            repeat_click_all_windows(dofus_windows, 1)
        if keyboard.is_pressed('f6'):
            while keyboard.is_pressed('f6'):
                time.sleep(0.1)
            repeat_click_all_windows(dofus_windows, 2, 0)
        if keyboard.is_pressed('f2'):
            while keyboard.is_pressed('f2'):
                time.sleep(0.1)
            end_turn_and_next()
        if keyboard.is_pressed('f8'):
            while keyboard.is_pressed('f8'):
                time.sleep(0.1)
            current_index = 9

def queue_setup():
    load_queue()
    print("Press 'y' to define the queue, 'n' to continue")
    input_ = input()
    if input_ == 'y':
        define_queue()
        save_queue()
    else:
        print("Queue already defined")

if __name__ == "__main__":
    main()
