import pyautogui
import time
from itertools import cycle
#pyautogui.moveTo(100,100,duration=0.5)


def click():
    time.sleep(10)
    pyautogui.click()

def click_forever():
    for _ in cycle(range(10)):
        print(pyautogui.position())
        click()

def pick_and_flower():
    init_x, init_y = pyautogui.position()

    while True:
        total_flowers = 4
        while total_flowers > 0:
            #pyautogui.press('f')
            click()
            pyautogui.moveTo(init_x + 100, init_y + 100, duration=0.5)
            total_flowers -= 1

if __name__ == "__main__":
    click_forever()
    #pick_and_flower()