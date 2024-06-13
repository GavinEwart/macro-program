import json
import os
import threading
import time
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import keyboard  # For global hotkey
import pygetwindow as gw  # For window management

MACRO_FILE = 'macros.json'

class MacroManager:
    def __init__(self):
        self.macros = self.load_macros()
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.running_macros = []
        self.global_running = True
        self.setup_kill_switch()
        self.target_window = None

    def setup_kill_switch(self):
        keyboard.add_hotkey('ctrl+shift+esc', self.emergency_stop)

    def emergency_stop(self):
        self.global_running = False
        self.running_macros.clear()
        print("Emergency stop activated: All macros terminated")

    def set_target_window(self, window_title):
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            self.target_window = windows[0]
            self.target_window.activate()

    def add_macro(self, macro):
        self.macros.append(macro)

    def get_macros(self):
        return self.macros

    def get_macro(self, index):
        return self.macros[index]

    def start_macro(self, macro):
        if self.global_running and self.target_window:
            self.target_window.activate()
            macro_thread = threading.Thread(target=self.run_macro, args=(macro,))
            self.running_macros.append(macro_thread)
            macro_thread.start()

    def stop_macro(self):
        self.global_running = False
        for thread in self.running_macros:
            if thread.is_alive():
                thread.join()

    def run_macro(self, macro):
        while self.global_running:
            for action in macro["actions"]:
                if not self.global_running:
                    break
                if action["condition"] == "held":
                    self.run_action(action)
                elif action["condition"] == "unheld":
                    self.run_action(action)
                elif action["condition"] == "press":
                    self.run_action(action)
                    break
                elif action["condition"] == "release":
                    self.run_action(action)
                    break
                elif action["condition"] == "double":
                    self.run_action(action)
                    break
                elif action["condition"] == "tap":
                    self.run_action(action)
                    break
                elif action["condition"] == "hold":
                    self.run_action(action)
                    break
                if action["repeat"]:
                    while self.global_running:
                        self.run_action(action)

    def run_action(self, action):
        if action["type"] == "key_press":
            self.press_key(action["key"], action["duration"])
        elif action["type"] == "key_release":
            self.release_key(action["key"], action["duration"])
        elif action["type"] == "mouse_click":
            self.click_mouse(action["key"], action["duration"])
        elif action["type"] == "wait":
            time.sleep(action["duration"] / 1000)

    def press_key(self, key, duration):
        self.keyboard.press(key)
        time.sleep(duration / 1000)
        self.keyboard.release(key)
        print(f"Pressed key: {key} for {duration} ms")

    def release_key(self, key, duration):
        self.keyboard.release(key)
        time.sleep(duration / 1000)
        print(f"Released key: {key} for {duration} ms")

    def click_mouse(self, button, duration):
        mouse_button = {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle
        }.get(button, Button.left)
        self.mouse.press(mouse_button)
        time.sleep(duration / 1000)
        self.mouse.release(mouse_button)
        print(f"Clicked mouse button: {button} for {duration} ms")

    def load_macros(self):
        if os.path.exists(MACRO_FILE):
            with open(MACRO_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_macros(self):
        with open(MACRO_FILE, 'w') as file:
            json.dump(self.macros, file, indent=4)
