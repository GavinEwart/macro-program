# Macro Program

## Overview

This Macro Program allows you to create and manage macros for keyboard and mouse actions. You can configure macros to run in any selected open program window. The program features a modern, dark-themed UI and includes a global kill switch to stop all macros instantly.

## Features

- Create, edit, and delete macros.
- Configure key presses, key releases, mouse clicks, and wait actions.
- Set conditions like held, unheld, press, release, double, tap, and hold for actions.
- Select an open program window to run macros.
- Dark mode UI using `ttkthemes`.
- Global kill switch using `Ctrl + Shift + Esc` to stop all macros.

## Requirements

- Python 3.x
- `pynput` for keyboard and mouse control.
- `keyboard` for global hotkey.
- `pygetwindow` for window management.
- `ttkthemes` for dark mode UI.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/your-repository/macro_program.git
    cd macro_program
    ```

2. **Set Up Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Program**:

    ```bash
    python src/main.py
    ```

2. **Creating a Macro**:

    - Click the "Add Macro" button to create a new macro.
    - Edit the macro name and add actions such as key presses, mouse clicks, and wait actions.
    - Configure conditions and duration for each action.
    - Save the macro.

3. **Selecting a Target Window**:

    - Click the "Refresh Window List" button to list all open windows.
    - Select a window from the list and click "Select Window" to set it as the target for the macros.

4. **Starting and Stopping Macros**:

    - Select a macro from the list and click "Start Macro" to run it in the selected window.
    - Click "Stop Macro" to stop the currently running macro.

5. **Emergency Stop**:

    - Press `Ctrl + Shift + Esc` at any time to stop all macros immediately.

## Notes

- Ensure you have the necessary permissions to control the selected window.
- Use the global kill switch responsibly to avoid unintended behavior.

## Contributing

- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Commit your changes (`git commit -am 'Add new feature'`).
- Push to the branch (`git push origin feature-branch`).
- Create a new Pull Request.

## License

This project is licensed under the MIT License.
