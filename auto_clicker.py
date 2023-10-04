import pyautogui
import time
from itertools import cycle
import pygetwindow as gw
import threading
import time
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class ClickerThread(threading.Thread):
    def __init__(self, window, click_speed, click_state_callback):
        super(ClickerThread, self).__init__()
        self._stop_event = threading.Event()
        self.window = window
        self.click_speed = click_speed
        self.click_state_callback = click_state_callback

    def run(self):
        print("Thread is running...")
        while not self._stop_event.is_set():
            current_app = get_active_app()
            if self.window == current_app:
                pyautogui.click()
                formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Clicked at Time:", formatted_time)
                print(f"Sleeping for {float(self.click_speed)} seconds")
                time.sleep(float(self.click_speed))
                self.click_state_callback(True)
            else:
                self.click_state_callback(False)

    def stop(self):
        self._stop_event.set()


def get_active_app():
    try:
        return active_window.title if (active_window := gw.getActiveWindow()) else ''
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_open_windows():
    # Get all open windows
    return gw.getAllTitles()


class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        self.is_running = False

        # Set the size of the window to a fixed value (width x height)
        self.root.geometry("400x200")

        # Disallow resizing
        root.resizable(False, False)

        # Create and configure the toggle button
        self.toggle_button = tk.Button(root, text="Start", command=self.toggle)
        self.toggle_button.pack(pady=10)

        # Create and configure the dropdown
        self.options = sorted([item for item in get_open_windows() if item])
        self.selected_option = tk.StringVar()
        self.combobox = ttk.Combobox(
            root, textvariable=self.selected_option, values=self.options, width=200, state="readonly")
        self.combobox.pack(padx=10, pady=10)

        # Validation function to allow only float input
        self.float_validator = root.register(self.validate_float)

        # Click state
        self.click_state = ttk.Label(
            root, text="Click State: Not Clicking", foreground='red')
        self.click_state.pack(pady=10)

        # Create a label
        label = ttk.Label(root, text="Click Speed (in seconds):")
        label.pack(pady=10)

        # Create an entry box for floating-point numbers
        self.click_speed = ttk.Entry(root, validate="key",
                                     validatecommand=(self.float_validator, "%P"))
        self.click_speed.pack(pady=10)
        self.click_speed.insert(0, '1.0')  # set default to 1.0

        self.clicker_instance = None

    def validate_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def update_click_state(self, is_clicking):
        if is_clicking:
            self.click_state.config(text="Click State: Clicking")
            self.click_state.config(foreground="green")
        else:
            self.click_state.config(text="Click State: Not Clicking")
            self.click_state.config(foreground="red")

    def disable_combobox(self):
        self.combobox.state(["disabled"])

    def enable_combobox(self):
        self.combobox.state(["!disabled"])

    def disable_click_speed_entry(self):
        self.click_speed.config(state="disabled")

    def enable_click_speed_entry(self):
        self.click_speed.config(state="normal")

    def toggle(self):
        if not self.selected_option.get():
            return
        if self.is_running:
            self.stop()
        else:
            self.start()

    def start(self):
        self.is_running = True
        self.toggle_button.configure(text="Stop")

        self.clicker_instance = ClickerThread(
            self.selected_option.get(), self.click_speed.get(), self.update_click_state)
        self.clicker_instance.start()
        self.disable_combobox()
        self.disable_click_speed_entry()

    def stop(self):
        self.is_running = False
        self.toggle_button.configure(text="Start")
        if self.clicker_instance:
            self.clicker_instance.stop()
        self.enable_combobox()
        self.enable_click_speed_entry()


global instance


def on_closing():
    # This function will be called when the window is closed
    print("Cleanup function called")
    instance.stop()
    root.destroy()


# Create the main window
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)


# Create an instance of the GUI
instance = AutoClickerGUI(root)


# Start the Tkinter event loop
root.mainloop()
