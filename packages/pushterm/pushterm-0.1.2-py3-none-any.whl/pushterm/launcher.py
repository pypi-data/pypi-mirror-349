# launcher.py
from .terminal_ui import launch_terminal

if __name__ == "__main__":
    launch_terminal()
# pushterm/launcher.py
def main():
    from terminal_ui import start_terminal_ui
    start_terminal_ui()  # Or whatever launches your terminal UI


if __name__ == "__main__":
    main()
