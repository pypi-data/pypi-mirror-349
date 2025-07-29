import sys
import time
import textwrap
import ast
import inspect
import ast
import subprocess
import tempfile
import os
import ast
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QLabel, QCheckBox, QRadioButton, QButtonGroup,
                             QLineEdit, QMessageBox, QDialog, 
                             QVBoxLayout, QTextEdit)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IKcode GUI terminal connector - v1.0.PyQt5")
        self.setGeometry(100, 100, 800, 800)
        self.setWindowIcon(QIcon("ikcode.png"))
        self.setStyleSheet("background-color: #1a7689;")

        self.checkbox = QCheckBox("Connect to terminal", self)

        self.blabel = QLabel("   GUI disabled", self)

        self.radio1 = QRadioButton("Record to server log", self)
        self.radio2 = QRadioButton("Do not record to server log", self)

        self.button_group = QButtonGroup(self)

        label = QLabel("IKcode GUI", self)
        label.setFont(QFont("Veranda", 18, QFont.Bold))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet("color: white; background-color: #1a7689; border: 2px solid #ffcc00;")
        label.setAlignment(Qt.AlignCenter)

        self.rlabel = QLabel("Server preferences:", self)
        self.rlabel.setGeometry(10, 500, 500, 100)
        self.rlabel.setStyleSheet("color: white; background-color: #1a7689; font-size:20px; font-family: Veranda;")

        self.tlabel = QLabel("Connect to your \n IKcode account:", self)
        self.tlabel.setGeometry(600, 50, 200, 50)
        self.tlabel.setStyleSheet("color: white; background-color: #1a7689; font-size:16px; font-family: Veranda;")
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(600, 100, 150, 30)
        self.textbutton = QPushButton("Connect", self)
        self.textbutton.setGeometry(600, 140, 150, 30)

        self.cbutton = QPushButton("View CheckInfo", self)
        self.cbutton.setGeometry(300, 410, 200, 50)
        self.cbutton.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")

        self.initUI()

        pixmap = QPixmap("ikcode.png")
        picture_label = QLabel(self)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        picture_label.setPixmap(scaled_pixmap)
        picture_label.setGeometry(500, 0, 100, 100)
        picture_label.setAlignment(Qt.AlignCenter)

    def initUI(self):
        # Enable GUI / Disable GUI button
        self.button = QPushButton("Enable GUI", self)
        self.button.setGeometry(300, 150, 200, 50)
        self.button.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.button.clicked.connect(self.on_click)

        # Centered View File Info button
        self.info_button = QPushButton("View File Info", self)
        self.info_button.setGeometry(300, 350, 200, 50)  # roughly center horizontally at 800 width window
        self.info_button.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.info_button.clicked.connect(self.view_file_info)

        # Help button bottom right
        self.help_button = QPushButton("Help", self)
        self.help_button.setGeometry(690, 740, 100, 50)
        self.help_button.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.help_button.clicked.connect(self.help_button_clicked)

        self.blabel.setGeometry(300, 210, 200, 50)
        self.blabel.setStyleSheet("background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")

        self.checkbox.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.checkbox.setGeometry(300, 270, 200, 50)
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.checkbox_changed)

        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.radio1)
        self.radio_group.addButton(self.radio2)

        self.radio1.setGeometry(10, 610, 200, 50)
        self.radio1.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.radio1.clicked.connect(self.radio1_checked)
        self.radio1.setChecked(True)
        self.log = True

        self.radio2.setGeometry(10, 670, 200, 50)
        self.radio2.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.radio2.clicked.connect(self.radio2_checked)

        self.button_group.addButton(self.radio1)
        self.button_group.addButton(self.radio2)

        self.textbox.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.textbutton.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.textbutton.clicked.connect(self.textbutton_clicked)

        self.cbutton.clicked.connect(self.view_check_info)

    def on_click(self):
        self.blabel.setText("   GUI enabled")
        self.button.setText("Disable GUI")
        try:
            self.button.clicked.disconnect()
        except Exception:
            pass
        self.button.clicked.connect(self.off_click)

    def off_click(self):
        self.blabel.setText("   GUI disabled")
        self.button.setText("Enable GUI")
        try:
            self.button.clicked.disconnect()
        except Exception:
            pass
        self.button.clicked.connect(self.on_click)

    def checkbox_changed(self, state):
        if self.log:
            if state == Qt.Checked:
                print("\nTerminal connected")
                if self.button.text() == "Disable GUI" and self.checkbox.isChecked():
                    print("\nGUI successfully connected to terminal")
                    self.blabel.setText("   GUI enabled")
            else:
                print("\nTerminal disconnected")
                if self.button.text() == "Disable GUI" and not self.checkbox.isChecked():
                    print("\nGUI disconnected from terminal")

    def radio1_checked(self):
        self.log = True
        print("\nServer log enabled")

    def radio2_checked(self):
        self.log = False
        print("\nServer log disabled")

    def help_button_clicked(self):
        help_text = """
    IKcode GUI Terminal Connector - User Guide

    Welcome to the IKcode GUI Terminal Connector! This application allows you to connect your GUI to a terminal session, manage server logging preferences, and analyze your Python code functions with the powerful CheckInfo feature.

    Enabling the GUI
    - Click the Enable GUI button to activate the GUI.
    - When enabled, the label below the button changes to GUI enabled, and the button text switches to Disable GUI.
    - To disable the GUI, simply click the button again.

    Connecting to the Terminal
    - To connect the GUI to the terminal, check the Connect to terminal checkbox.
    - You must first enable the GUI before connecting to the terminal.
    - When connected, the label will confirm the GUI is connected.

    Server Logging Preferences
    - Choose whether to record interactions to the server log.
    - Use the two radio buttons:
    - Record to server log — enables logging.
    - Do not record to server log — disables logging.
    - By default, logging is enabled.

    Connecting to Your IKcode Account
    - Enter your IKcode account name or ID in the text box labeled Connect to your IKcode account.
    - Click the Connect button to simulate connection.
    - The application will display connection progress messages in the terminal output.

    CheckInfo Feature
    - CheckInfo is a Python decorator that analyzes a function’s code to gather useful details like variable names, imports, classes, loops, and more.
    - Add @CheckInfo above any function you want to analyze.
    - After decorating, access the info via function._checkinfo_instance.get_info() or click 'View CheckInfo' in the GUI.
    - Remember to enable and connect the GUI first!

    For more, visit: https://ikgtc.pythonanywhere.com/help 
    """

        if self.log:
            print(help_text)

        dialog = QDialog(self)
        dialog.setWindowTitle("Help - IKcode GUI Terminal Connector")
        dialog.resize(600, 400)  # Adjust size as needed

        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit(dialog)
        text_edit.setReadOnly(True)
        text_edit.setPlainText(help_text)
        layout.addWidget(text_edit)

        close_btn = QPushButton("Close", dialog)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()


    def textbutton_clicked(self):
        text = self.textbox.text()

        if self.log:
            time.sleep(0.3)
            print("\nConnecting to IKcode account...")
            time.sleep(2.7)
            print(f"\nConnected to IKcode account: {text}\n")

    def view_file_info(self):
        # Check if GUI enabled and terminal connected
        gui_enabled = self.button.text() == "Disable GUI"
        terminal_connected = self.checkbox.isChecked()
        if not (gui_enabled and terminal_connected):
            QMessageBox.warning(self, "Error", "GUI must be enabled and terminal connected to view file info.")
            return

        # Get current running file path
        try:
            filename = os.path.abspath(sys.argv[0])
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")
            return

        try:
            tree = ast.parse(code)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse file:\n{e}")
            return

        all_info = {}

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                analyzer = CodeAnalyzer()
                analyzer.visit(node)
                all_info[node.name] = {
                    "Function Names": analyzer.function_names,
                    "Variable Names": analyzer.variable_names,
                    "Imports": analyzer.imports,
                    "Classes": analyzer.classes,
                    "Loops": analyzer.loops,
                    "Conditionals": analyzer.conditionals,
                    "Comments": analyzer.comments
                }

        # Format info for display
        output = ""
        for func_name, info in all_info.items():
            # Filtering: skip if only function itself in Function Names and no classes/imports/loops/conditionals/comments
            only_self_function = info["Function Names"] == [func_name]
            other_keys_empty = all(not info[key] for key in ["Classes", "Imports", "Loops", "Conditionals", "Comments"])

            if only_self_function and other_keys_empty:
                # Skip printing this function info block
                continue

            output += f"Function: {func_name}\n"
            for key, values in info.items():
                value_str = ", ".join(values) if values else "None"
                output += f"  {key}: {value_str}\n"
            output += "\n"

        # Split code into lines for stats
        lines = code.splitlines()
        code_length = len(lines)

        # Count functions and classes via ast parsing
        try:
            tree = ast.parse(code)
            function_count = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
            class_count = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
        except Exception:
            function_count = 0
            class_count = 0

        # Count comment lines and blank lines
        comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
        blank_lines = sum(1 for line in lines if not line.strip())

        # Basic lint check: Try compiling
        try:
            compile(code, filename, 'exec')
            lint_errors = "No syntax errors detected."
        except SyntaxError as e:
            lint_errors = f"Syntax Error: {e}"

        # Get date and time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        info_text = (
            f"Date and time: {now}\n"
            f"File route: {filename}\n"
            f"File name: {os.path.basename(filename)}\n"
            f"Lines of code: {code_length}\n"
            f"Function definitions: {function_count}\n"
            f"Class definitions: {class_count}\n"
            f"Comment lines: {comment_lines}\n"
            f"Blank lines: {blank_lines}\n"
            f"Lint check: {lint_errors}\n"
            "==========================\n"
            
        )

        # Print to terminal if server log enabled
        if self.log:
            print("\n=== File Info ===")
            print(info_text)
            print("=================\n")

        # Show info in message box
        QMessageBox.information(self, "File Info", info_text)

    def view_check_info(self):
    # Check if GUI enabled and terminal connected
        gui_enabled = self.button.text() == "Disable GUI"
        terminal_connected = self.checkbox.isChecked()
        if not (gui_enabled and terminal_connected):
            QMessageBox.warning(self, "Error", "GUI must be enabled and terminal connected to view check info.")
            return

        # Get current running file path
        try:
            filename = os.path.abspath(sys.argv[0])
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")
            return

        try:
            tree = ast.parse(code)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse file:\n{e}")
            return

        all_info = {}

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                analyzer = CodeAnalyzer()
                analyzer.visit(node)
                all_info[node.name] = {
                    "Function Names": analyzer.function_names,
                    "Variable Names": analyzer.variable_names,
                    "Imports": analyzer.imports,
                    "Classes": analyzer.classes,
                    "Loops": analyzer.loops,
                    "Conditionals": analyzer.conditionals,
                    "Comments": analyzer.comments
                }

        # Format output for CheckInfo only, skipping trivial functions
        output = ""
        for func_name, info in all_info.items():
            only_self_function = info["Function Names"] == [func_name]
            other_keys_empty = all(not info[key] for key in ["Classes", "Imports", "Loops", "Conditionals", "Comments"])

            if only_self_function and other_keys_empty:
                continue

            output += f"Function: {func_name}\n"
            for key, values in info.items():
                value_str = ", ".join(values) if values else "None"
                output += f"  {key}: {value_str}\n"
            output += "\n"

        if not output:
            output = "No detailed CheckInfo data found for any function."

        # Show info in message box (only CheckInfo data)
        QMessageBox.information(self, "CheckInfo", output)




full_info = {}

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_names = []
        self.variable_names = []
        self.imports = []
        self.classes = []
        self.loops = []
        self.conditionals = []
        self.comments = []

    def visit_FunctionDef(self, node):
        self.function_names.append(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variable_names.append(target.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_For(self, node):
        self.loops.append('for')
        self.generic_visit(node)

    def visit_While(self, node):
        self.loops.append('while')
        self.generic_visit(node)

    def visit_If(self, node):
        self.conditionals.append('if')
        self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            self.comments.append(node.value.value)
        self.generic_visit(node)



class CheckInfo:
    def __init__(self, func):
        self.func = func
        self.full_info = {}
        self._analyze_code()

        # Attach self to the function object for easy access
        setattr(self.func, "_checkinfo_instance", self)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


    def _analyze_code(self):
        source_lines, _ = inspect.getsourcelines(self.func)
        source = "".join(source_lines)

        tree = ast.parse(source)
        analyzer = CodeAnalyzer()

        func_node = None
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == self.func.__name__:
                func_node = node
                break

        if func_node is None:
            analyzer.visit(tree)  # fallback, analyze everything
        else:
            analyzer.visit(func_node)  # analyze entire function node subtree

        self.full_info = {
            "Function Names": analyzer.function_names,
            "Variable Names": analyzer.variable_names,
            "Imports": analyzer.imports,
            "Classes": analyzer.classes,
            
        }

    def get_info(self):
        return self.full_info

def Help(topic=None):
    general_help = """
Welcome to IKcode GTconnect!

This package includes:
  • CheckInfo — a Python decorator to analyze function internals.
  • runGUI — launch a GUI terminal connector to interact with the tool visually.
  • Help — view usage documentation.

How to import:

    from ikcode_gtconnect import CheckInfo, runGUI, Help

How to use CheckInfo:

    @CheckInfo
    def my_function():
        pass

    info = my_function._checkinfo_instance.get_info()
    print(info)

To run the GUI:

    runGUI()

For more specific help:

    Help(CheckInfo)      # Help on CheckInfo
    Help(runGUI)         # Help on the GUI
    Help("gui")          # Help on the GUI

Or to see more, visit: https://ikgtc.pythonanywhere.com/help 
"""

    gui_help = """
IKcode GUI Terminal Connector - GUI Help

To use the GUI:

1. Import and run:
       from ikcode_gtconnect import runGUI
       runGUI()

2. Enable GUI:
       Click "Enable GUI" to activate.

3. Connect to terminal:
       Check the "Connect to terminal" checkbox (after enabling GUI).

4. Server logging:
       Use radio buttons to toggle logging.

5. CheckInfo button:
       Click 'View CheckInfo' to display analysis (must decorate a function first).
"""

    checkinfo_help = """
CheckInfo - Decorator Help

Purpose:
    Analyze a function’s code to extract info on variables, loops, imports, etc.

Usage:
    from ikcode_gtconnect import CheckInfo

    @CheckInfo
    def my_func():
        x = 5
        for i in range(x):
            print(i)

    info = my_func._checkinfo_instance.get_info()
    print(info)

Methods:
    get_info() — returns a dictionary of code analysis

Note:
    CheckInfo only works on user-defined functions.
"""

    # Dispatcher logic
    if topic is None:
        print(general_help)
    elif isinstance(topic, str) and topic.lower() == "gui":
        print(gui_help)
    elif topic.__name__ == "runGUI":
        print(gui_help)
    elif topic.__name__ == "CheckInfo":
        print(checkinfo_help)
    else:
        print("Unrecognized help topic. Try Help(), Help(CheckInfo), or Help(runGUI).")

def show_help():
    print("""
IKcode GTconnect - Help Guide

This package provides both a graphical interface and a Python utility to analyze your code.

USAGE:
    ikcode-gtconnect                Launch the GUI
    ikcode-gtconnect --help         Show this help guide

FEATURES:

1. GUI Terminal Connector
   • Connect GUI to your terminal session
   • Toggle server logging
   • Link to your IKcode account
   • View CheckInfo output

2. CheckInfo Python Decorator
   • Use @CheckInfo on any function to analyze it
   • Access info with: my_function._checkinfo_instance.get_info()
   • Can be used standalone, or viewed via GUI

3. Help Function (in Python)
   >>> from ikcode_gtconnect import Help
   >>> Help()                   # General help
   >>> Help(runGUI)            # GUI help
   >>> Help(CheckInfo)         # CheckInfo help
          
4. Current methods:
    • CheckInfo                # Decorator to analyze function
    • runGUI                   # Launch the GUI
    • Help                     # View help for a specific topic

For more, visit: https://ikgtc.pythonanywhere.com/help 
""")


def runGUI():
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        sys.exit(0)  # exit immediately, no GUI launched

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


@CheckInfo
def test():
    print("yo")
    def yo():
        print("yo")

    

if __name__ == "__main__":
    print("\n\nIKcode GUI terminal connector\n")
    print("Server log:\n")
    runGUI()
