import os
import platform
import winsound

def play_beep():
    # Get the current operating system
    current_os = platform.system().lower()

    if current_os == "linux": # Linux
        os.system("beep")
    
    elif current_os == "darwin": # macOS
        os.system("osascript -e 'beep'")

    elif current_os == "windows":
        winsound.MessageBeep() #requires windsound
    else:
        print(f"Unsupported OS: {current_os}")
