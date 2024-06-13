import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from macro_manager import MacroManager
import pygetwindow as gw

class MacroProgram:
    def __init__(self):
        self.root = ThemedTk(theme="equilux")
        self.root.title("Macro Program")
        self.macro_manager = MacroManager()
        self.create_gui()

    def create_gui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.add_macro_button = ttk.Button(self.main_frame, text="Add Macro", command=self.add_macro)
        self.add_macro_button.grid(row=0, column=0, pady=5)

        self.macro_listbox = tk.Listbox(self.main_frame, height=15, width=50)
        self.macro_listbox.grid(row=1, column=0, pady=5)

        self.start_macro_button = ttk.Button(self.main_frame, text="Start Macro", command=self.start_macro)
        self.start_macro_button.grid(row=2, column=0, pady=5)

        self.stop_macro_button = ttk.Button(self.main_frame, text="Stop Macro", command=self.stop_macro)
        self.stop_macro_button.grid(row=3, column=0, pady=5)

        self.edit_macro_button = ttk.Button(self.main_frame, text="Edit Macro", command=self.edit_macro)
        self.edit_macro_button.grid(row=4, column=0, pady=5)

        self.kill_switch_button = ttk.Button(self.main_frame, text="Kill Switch", command=self.kill_switch)
        self.kill_switch_button.grid(row=5, column=0, pady=5)

        self.window_listbox = tk.Listbox(self.main_frame, height=10, width=50)
        self.window_listbox.grid(row=6, column=0, pady=5)

        self.refresh_windows_button = ttk.Button(self.main_frame, text="Refresh Window List", command=self.refresh_window_list)
        self.refresh_windows_button.grid(row=7, column=0, pady=5)

        self.select_window_button = ttk.Button(self.main_frame, text="Select Window", command=self.select_window)
        self.select_window_button.grid(row=8, column=0, pady=5)

        self.refresh_window_list()

    def add_macro(self):
        new_macro = {"name": "New Macro", "actions": []}
        self.macro_manager.add_macro(new_macro)
        self.update_macro_listbox()
        print(f"Added new macro: {new_macro}")

    def update_macro_listbox(self):
        self.macro_listbox.delete(0, tk.END)
        for macro in self.macro_manager.get_macros():
            self.macro_listbox.insert(tk.END, macro["name"])

    def start_macro(self):
        selected_macro_index = self.macro_listbox.curselection()
        if selected_macro_index:
            macro = self.macro_manager.get_macro(selected_macro_index[0])
            self.macro_manager.start_macro(macro)
            print(f"Started macro: {macro}")

    def stop_macro(self):
        self.macro_manager.stop_macro()
        print("Stopped macro")

    def edit_macro(self):
        selected_macro_index = self.macro_listbox.curselection()
        if selected_macro_index:
            macro = self.macro_manager.get_macro(selected_macro_index[0])
            self.open_macro_editor(macro)

    def open_macro_editor(self, macro):
        editor = MacroEditor(self.root, macro, self.update_macro_listbox)

    def kill_switch(self):
        self.macro_manager.emergency_stop()
        self.root.quit()
        print("Kill switch activated: Stopped all macros and closed the program")

    def refresh_window_list(self):
        self.window_listbox.delete(0, tk.END)
        for window in gw.getAllTitles():
            if window:
                self.window_listbox.insert(tk.END, window)

    def select_window(self):
        selected_window_index = self.window_listbox.curselection()
        if selected_window_index:
            window_title = self.window_listbox.get(selected_window_index)
            self.macro_manager.set_target_window(window_title)
            print(f"Selected window: {window_title}")

    def run(self):
        self.root.mainloop()

class MacroEditor:
    def __init__(self, parent, macro, update_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Edit Macro")
        self.macro = macro
        self.update_callback = update_callback

        self.name_label = ttk.Label(self.top, text="Macro Name")
        self.name_label.grid(row=0, column=0, pady=5)
        self.name_entry = ttk.Entry(self.top)
        self.name_entry.grid(row=0, column=1, pady=5)
        self.name_entry.insert(0, self.macro["name"])

        self.action_frame = ttk.Frame(self.top)
        self.action_frame.grid(row=1, column=0, columnspan=2, pady=5)
        self.action_canvas = tk.Canvas(self.action_frame)
        self.action_scrollbar = ttk.Scrollbar(self.action_frame, orient="vertical", command=self.action_canvas.yview)
        self.action_scrollable_frame = ttk.Frame(self.action_canvas)

        self.action_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.action_canvas.configure(
                scrollregion=self.action_canvas.bbox("all")
            )
        )

        self.action_canvas.create_window((0, 0), window=self.action_scrollable_frame, anchor="nw")
        self.action_canvas.configure(yscrollcommand=self.action_scrollbar.set)

        self.action_canvas.pack(side="left", fill="both", expand=True)
        self.action_scrollbar.pack(side="right", fill="y")

        self.update_action_listbox()

        self.add_action_button = ttk.Button(self.top, text="Add Action", command=self.add_action)
        self.add_action_button.grid(row=2, column=0, pady=5)
        self.remove_action_button = ttk.Button(self.top, text="Remove Action", command=self.remove_action)
        self.remove_action_button.grid(row=2, column=1, pady=5)

        self.save_button = ttk.Button(self.top, text="Save", command=self.save_macro)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=5)

    def update_action_listbox(self):
        for widget in self.action_scrollable_frame.winfo_children():
            widget.destroy()
        for i, action in enumerate(self.macro["actions"]):
            label = ttk.Label(self.action_scrollable_frame, text=str(action))
            label.grid(row=i, column=0, pady=5, sticky="w")

    def add_action(self):
        self.action_dialog = ActionDialog(self.top, self.macro, self.update_action_listbox)

    def remove_action(self):
        selected_action_index = self.action_listbox.curselection()
        if selected_action_index:
            del self.macro["actions"][selected_action_index[0]]
            self.update_action_listbox()

    def save_macro(self):
        self.macro["name"] = self.name_entry.get()
        self.update_callback()
        self.top.destroy()

class ActionDialog:
    def __init__(self, parent, macro, update_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Add Action")
        self.macro = macro
        self.update_callback = update_callback

        self.action_type_label = ttk.Label(self.top, text="Action Type")
        self.action_type_label.grid(row=0, column=0, pady=5)
        self.action_type = ttk.Combobox(self.top, values=["key_press", "key_release", "mouse_click", "wait"], state="readonly")
        self.action_type.grid(row=0, column=1, pady=5)
        self.action_type.bind("<<ComboboxSelected>>", self.show_options)

        self.key_label = ttk.Label(self.top, text="Key/Mouse Button")
        self.key_entry = ttk.Entry(self.top)

        self.duration_label = ttk.Label(self.top, text="Duration (ms)")
        self.duration_slider = ttk.Scale(self.top, from_=0, to=500, orient='horizontal', command=self.update_slider_label)
        self.duration_value_label = ttk.Label(self.top, text="0 ms")

        self.condition_label = ttk.Label(self.top, text="Condition")
        self.condition = ttk.Combobox(self.top, values=["held", "unheld", "press", "release", "double", "tap", "hold"], state="readonly")

        self.toggle_button = ttk.Button(self.top, text="Toggle Repeat", command=self.toggle_repeat)
        self.add_button = ttk.Button(self.top, text="Add", command=self.add_action)

        self.is_repeat = False

    def show_options(self, event):
        for widget in self.top.winfo_children():
            widget.grid_forget()
        self.action_type_label.grid(row=0, column=0, pady=5)
        self.action_type.grid(row=0, column=1, pady=5)
        action_type = self.action_type.get()

        if action_type in ["key_press", "key_release", "mouse_click"]:
            self.key_label.grid(row=1, column=0, pady=5)
            self.key_entry.grid(row=1, column=1, pady=5)
            self.duration_label.grid(row=2, column=0, pady=5)
            self.duration_slider.grid(row=2, column=1, pady=5)
            self.duration_value_label.grid(row=2, column=2, pady=5)
            self.condition_label.grid(row=3, column=0, pady=5)
            self.condition.grid(row=3, column=1, pady=5)
            self.toggle_button.grid(row=4, column=0, columnspan=2, pady=5)
            self.add_button.grid(row=5, column=0, columnspan=3, pady=5)
        elif action_type == "wait":
            self.duration_label.grid(row=1, column=0, pady=5)
            self.duration_slider.grid(row=1, column=1, pady=5)
            self.duration_value_label.grid(row=1, column=2, pady=5)
            self.add_button.grid(row=2, column=0, columnspan=3, pady=5)

    def update_slider_label(self, value):
        self.duration_value_label.config(text=f"{int(float(value))} ms")

    def toggle_repeat(self):
        self.is_repeat = not self.is_repeat
        print(f"Toggle repeat: {self.is_repeat}")

    def add_action(self):
        action_type = self.action_type.get()
        key = self.key_entry.get()
        duration = self.duration_slider.get()
        condition = self.condition.get()

        if action_type == "wait":
            action = {"type": action_type, "duration": int(duration)}
        elif action_type and key and condition:
            action = {
                "type": action_type,
                "key": key,
                "duration": int(duration),
                "condition": condition,
                "repeat": self.is_repeat
            }
        else:
            print("Missing required fields")
            return

        self.macro["actions"].append(action)
        self.update_callback()
        print(f"Added action: {action}")
        self.top.destroy()
