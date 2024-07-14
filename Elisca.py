# Voice-Controlled Virtual Assistant - VoiceGPT

# Description: Using speech recognition and text-to-speech capabilities, automating use of laptops.
# The assistant interacts with the user's voice input and performs actions accordingly.

# import necessary libraries
import pyttsx3                              # Library for text-to-speech conversion
import speech_recognition as sr             # Library for speech recognition
import wikipedia                            # Library for querying Wikipedia
import webbrowser                           # Library for opening web browser and URLs
import os                                   # Library for interacting with the operating system
import platform
import logging                              #for logging messages and debugging
import subprocess                           #to run external processes or commands
import shutil                               # Library for file operations (copy, move)
from PIL import Image                       # For working with images
from reportlab.pdfgen import canvas         # For generating PDFs
from reportlab.lib.pagesizes import letter  # Standard page size for PDFs
import docx2txt                             # For extracting text from Word documents
import zipfile                              # Library for working with ZIP archives
import datetime                             # For working with dates and times
import random                               # For generating random values
import psutil                               # For system monitoring and management
from googletrans import Translator          # For language translation using Google Translate
import traceback                            # For printing detailed error traceback
import socket                               # For network communication
from pathlib import Path                    #for working with file paths
import wmi                                  #for interacting with Windows Management Instrumentation (WMI)
import time                                 #for working with time-related functions
import getpass                              #to securely obtain the user's password
from ecapture import ecapture as ec         #to capture screenshots
import ctypes                               #for calling functions in dynamic link libraries (DLLs)
import smtplib                              #for handling SMTP (Simple Mail Transfer Protocol) for sending emails
import yagmail                              # Import the 'yagmail' library, a Python email client, for simplifying email sending tasks
from PIL import ImageGrab                   #for the conversion of image format
import getpass                              #for graph plotting
import matplotlib.pyplot as plt             #for data visulization
import urllib.request                       #for taking the request from server
from bs4 import BeautifulSoup               #for web scraping
import requests                             # for get and post request
import re                                   #for request for extrcating the mail
 

# Function to get user input for password creation
def create_password():
    while True:
        password = getpass.getpass("Create your password: ")
        confirm_password = getpass.getpass("Reenter your password for confirmation: ")

        if password == confirm_password:
            # Store the password in a file
            with open("password.txt", "w") as password_file:
                password_file.write(password)
            return password
        else:
            print("Passwords do not match. Please try again.")

# Function to authenticate the user with a password
def authenticate_user():
    # Check if the password file exists
    if os.path.exists("password.txt"):
        with open("password.txt", "r") as password_file:
            stored_password = password_file.read()
    else:
        # If the password file does not exist, create a new password
        stored_password = create_password()

    while True:
        entered_password = getpass.getpass("Enter your password: ")

        if entered_password == stored_password:
            print("Login successful!")
            break
        else:
            print("Incorrect password. Please try again.")

# Call the function to authenticate the user
authenticate_user()


# Define a dictionary to map file formats to their corresponding directories
# Customize this dictionary according to your desired file organization structure
DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "PYTHON": [".py",".pyi"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"]
}
FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}


# Function to open a specified folder
def open_folder(folder_name):
    try:
        user_os = platform.system()

        if user_os == 'Windows':
            command = 'chrome'
        elif user_os == 'Darwin':  # macOS
            command = 'open'
        elif user_os == 'Linux':
            command = 'xdg-open'
        else:
            speak("Sorry, your operating system is not supported for this operation.")
            return

        # Use the user's home directory as the search path
        search_path = os.path.expanduser("~")

        for root, dirs, files in os.walk(search_path):
            if folder_name in dirs:
                folder_path = os.path.join(root, folder_name)
                # Use subprocess.Popen to avoid command injection risks
                subprocess.Popen([command, folder_path])
                speak("Folder opened successfully.")
                break  # Break out of the loop once the folder is found
            else:
                speak(f"Sorry, I couldn't find the specified folder '{folder_name}'. Please check if it exists or not.")
                break  # Break out of the loop if the folder is not found
    except Exception as e:
        # Log the error
        logging.error(f"Error in open_folder: {e}")
        speak("Unable to open the folder.")



# Function to search for a file in a specified folder
def search_file_in_folder(folder_path, file_name):
    try:
        for root, dirs, files in os.walk(folder_path):
            if file_name in files:  # Check if the file name exists in the list of files
                return os.path.join(root, file_name)  # Return the complete path to the found file
        return None  # Return None if the file is not found in the specified folder
    except Exception as e:
        # Handle any exceptions that might occur during the search
        print(f"An error occurred while searching for the file: {e}")
        return None  # Return None in case of an error


# Function to convert image format
def convert_image_format(source_path, destination_path, new_format):
    try:
        # Open the source image using PIL (Python Imaging Library)
        image = Image.open(source_path)

        # Save the image in the specified new format at the destination path
        image.save(destination_path, new_format)

        # Call the "speak" function to provide feedback on successful conversion
        speak("Image converted successfully.")
    except Exception as e:
        # Print the error message and call the "speak" function for error feedback
        print(e)
        speak("Sorry, unable to convert the image.")


# Function to compress a file to a ZIP archive
def compress_to_zip(source_path, destination_path):
    try:
        # Open a ZIP archive for writing
        with zipfile.ZipFile(destination_path, 'w') as zipf:
            # Write the source file to the archive with its original filename
            zipf.write(source_path, os.path.basename(source_path))

        # Call the "speak" function to provide feedback on successful compression
        speak("File compressed to ZIP successfully.")
    except Exception as e:
        # Print the error message and call the "speak" function for error feedback
        print(e)
        speak("Unable to compress the file.")


# Function to convert a file to a different format
def convert_file_format(source_path, destination_path, new_format):
    try:
        # Check the target format and perform the appropriate conversion
        if new_format == 'PDF':
            # Convert Word document to PDF
            if source_path.lower().endswith('.docx'):
                convert_doc_to_pdf(source_path, destination_path)
            else:
                speak("Unsupported format for PDF conversion.")

        elif new_format == 'JPEG' or new_format == 'PNG':
            # Convert image to JPEG or PNG format
            if source_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                convert_image_format(source_path, destination_path, new_format)
            else:
                speak("Unsupported format for image conversion.")

        elif new_format == 'TXT':
            # Convert document or PDF to plain text
            if source_path.lower().endswith(('.docx', '.pdf')):
                convert_to_text(source_path, destination_path)
            else:
                speak("Unsupported format for text conversion.")

        # Add more conditions for other file formats and conversions
        else:
            speak("Unsupported conversion format.")

    except Exception as e:
        # Print the error message and call the "speak" function for error feedback
        print(e)
        speak("Sorry, unable to perform the conversion.")

# Function to compress a file
def compress_file(file_path):
    with zipfile.ZipFile(file_path + '.zip', 'w') as zipf:  # Open a ZIP file with write mode
        zipf.write(file_path, os.path.basename(file_path))  # Write the specified file to the ZIP file


# Function to convert document or PDF to plain text
def convert_to_text(source_path, destination_path):
    try:
        text = ""  # Initialize an empty string to hold the extracted text
        if source_path.lower().endswith('.docx'):
            text = docx2txt.process(source_path)  # Extract text from DOCX file
        elif source_path.lower().endswith('.pdf'):
            #Implement PDF to text conversion using appropriate library
            pass

        # Write the extracted text to the destination text file
        with open(destination_path, 'w') as text_file:
            text_file.write(text)

        speak("File converted to text successfully.")
    except Exception as e:
        # Print the error message and call the "speak" function for error feedback
        print(e)
        speak("Sorry, unable to convert the file to text.")


# Function to convert DOCX document to PDF format
def convert_doc_to_pdf(source_path, destination_path):
    try:
        # Extract content from the DOCX document
        content = docx2txt.process(source_path)

        # Define the PDF path by appending ".pdf" to the destination_path
        pdf_path = destination_path + ".pdf"

        # Create a canvas and generate a PDF from the extracted content
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(72, 720, content)  # Add the content to the PDF
        c.save()  # Finalize and save the PDF

        # Provide success feedback after conversion
        speak("Document converted to PDF successfully.")
    except Exception as e:
        # Print the error message and call the "speak" function for error feedback
        print(e)
        speak("Sorry, unable to convert the document to PDF.")


# Define a function to organize files based on the given criteria
#For example, move all image files to an "Images" folder, all music files to a "Music" folder, etc.
def organize_files(criteria):
    try:
        # Loop through all entries (files and directories) in the current directory
        for entry in os.scandir():
            if entry.is_dir():
                continue  # Skip directories, process files only

            # Get the file's path and format
            file_path = Path(entry.name)
            file_format = file_path.suffix.lower()

            # Check if the file format is in the FILE_FORMATS dictionary
            if file_format in FILE_FORMATS:
                # Get the target directory for the file format
                target_directory = Path(FILE_FORMATS[file_format])

                # Create the target directory if it doesn't exist
                target_directory.mkdir(exist_ok=True)

                # Move the file to the target directory
                new_path = target_directory.joinpath(file_path.name)
                file_path.rename(new_path)

        # Create an "OTHER" folder for files with unsupported formats
        os.mkdir("OTHER")

        # Loop through all entries in the current directory again
        for dir in os.scandir():
            try:
                if dir.is_dir():
                    os.rmdir(dir)  # Remove empty directories created during organization
                else:
                    # Move any remaining files to the "OTHER" directory
                    os.rename(dir.path, os.path.join("OTHER", dir.name))
            except Exception as e:
                print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to move a file from source to destination
def move_file(source_path, destination_path):
    try:
        if os.path.exists(source_path):
            os.rename(source_path, destination_path)  # Rename the file at the source path to the destination path
            print(f"File moved successfully from '{source_path}' to '{destination_path}'.")   # Inform the user that the file was moved successfully
        else:
            print(f"Source file '{source_path}' not found.")
    except Exception as e:
        print(f"Error while moving the file: {e}")     # Print the exception details if an error occurs
        print(f"Unable to move the file.")   # Inform the user that an error occurred while moving the file


# Function to copy a file from source to destination
def copy_file(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)  # Copy the file from the source path to the destination path
        speak("File copied successfully.")  # Inform the user that the file was copied successfully
    except Exception as e:
        print(e)  # Print the exception deta    ils if an error occurs
        speak("Unable to copy the file.")  # Inform the user that an error occurred while copying the file


# Function to rename a file
def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)  # Rename the file with the new name
        speak("File renamed successfully.")  # Inform the user that the file was renamed successfully
    except Exception as e:
        print(e)  # Print the exception details if an error occurs
        speak("Unable to rename the file.")  # Inform the user that an error occurred while renaming the file


# Define a function to change the display brightness to a specified percentage
def changeBrightness(brightness_percentage):
    try:
        # Create a WMI (Windows Management Instrumentation) object
        c = wmi.WMI(namespace='wmi')

        # Get the brightness methods for the monitor
        methods = c.WmiMonitorBrightnessMethods()[0]

        # Set the brightness to the specified percentage
        methods.WmiSetBrightness(brightness_percentage, 0)

        # Inform the user about the new brightness setting
        speak(f"Brightness set to {brightness_percentage}%")
    except Exception as e:
        # Handle any errors that occur while changing brightness
        speak("Error changing brightness:", str(e))


# Define a function to increase the display brightness
def increaseBrightness():
    try:
        # Create a WMI object
        c = wmi.WMI(namespace='wmi')

        # Get the brightness methods for the monitor
        methods = c.WmiMonitorBrightnessMethods()[0]

        # Get the current brightness level
        current_brightness = methods.WmiGetBrightness()[0]

        if current_brightness < 100:
            # Increase the brightness by 30 percentage points or adjust as needed
            new_brightness = min(current_brightness + 30, 100)

            # Set the new brightness level
            methods.WmiSetBrightness(new_brightness, 0)

            # Inform the user about the new brightness setting
            speak(f"Brightness increased to {new_brightness}%")
        else:
            # Inform the user that brightness is already at the maximum
            speak("Brightness is already at the maximum (100%). Cannot increase further.")
    except Exception as e:
        # Handle any errors that occur while changing brightness
        speak("Error changing brightness:", str(e))


# Define a function to decrease the display brightness
def decreaseBrightness():
    try:
        # Create a WMI object
        c = wmi.WMI(namespace='wmi')

        # Get the brightness methods for the monitor
        methods = c.WmiMonitorBrightnessMethods()[0]

        # Get the current brightness level
        current_brightness = methods.WmiGetBrightness()[0]

        if current_brightness > 0:
            # Decrease the brightness by 30 percentage points or adjust as needed
            new_brightness = max(current_brightness - 30, 0)

            # Set the new brightness level
            methods.WmiSetBrightness(new_brightness, 0)

            # Inform the user about the new brightness setting
            speak(f"Brightness decreased to {new_brightness}%")
        else:
            # Inform the user that brightness is already at the minimum
            speak("Brightness is already at the minimum (0%). Cannot decrease further.")
    except Exception as e:
        # Handle any errors that occur while changing brightness
        speak("Error changing brightness:", str(e))


# Function to check if internet connectivity is available
def internet_connected():
    try:
        # Attempt to resolve the Google DNS server address
        host = socket.gethostbyname("www.google.com")
        # Establish a connection to the Google DNS server
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


# Function to troubleshoot system issues
def troubleshoot_system():
    try:
        # Check for disk space availability
        disk_space = psutil.disk_usage('/')
        if disk_space.percent > 90:
            speak("Warning: Your disk space is almost full. Consider freeing up some space.")

        # Check for high CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            speak("Warning: High CPU usage detected. Check for resource-intensive processes.")

        # Check for high RAM usage
        ram_percent = psutil.virtual_memory().percent
        if ram_percent > 80:        
            speak("Warning: High RAM usage detected. Close unnecessary applications or processes.")

        # Check for internet connectivity
        if not internet_connected():
            speak("Warning: No internet connectivity detected. Check your network connection.")

        # Provide overall troubleshooting feedback
        speak("System troubleshooting complete. No critical issues found.")

    except Exception:
        # Handle errors during troubleshooting and print traceback
        speak("An error occurred while troubleshooting the system. Please check the logs for more information.")
        print(traceback.format_exc())
# Additional - function to fix the detected issues in system


# Function to retrieve system specifications
def get_system_specifications():
    # Gather CPU information
    cpu_info = {
        'CPU': f"{psutil.cpu_percent(interval=1)}% usage",
        'Cores': psutil.cpu_count(logical=False),
        'Threads': psutil.cpu_count(logical=True)
    }

    # Gather RAM information
    ram_info = {
        'Total RAM': f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        'Available RAM': f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
        'Used RAM': f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB"
    }

    # Gather disk storage information
    disk_info = {
        'Total Storage': f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
        'Free Storage': f"{psutil.disk_usage('/').free / (1024 ** 3):.2f} GB",
        'Used Storage': f"{psutil.disk_usage('/').used / (1024 ** 3):.2f} GB"
    }

    return cpu_info, ram_info, disk_info


# Function to check battery status
def check_battery_status():
    try:
        # Get battery information
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = battery.percent
        

        # Determine battery status based on whether it's plugged in
        status = "Plugged in" if plugged else "Not plugged in"

        # Provide feedback on battery status and percentage
        speak("Battery Status: " + status)
        print("Battery Status:", status)
        speak("Battery Percentage:" + str(percent) + "%")
        print("Battery Percentage:", percent, "%")

        # Provide alerts based on battery level and charging status
        if percent < 20 and not plugged:
            speak("Alert: Battery is running low! Consider connecting to a power source.")
            print("Alert: Battery is running low! Consider connecting to a power source.")
        elif percent == 100 and plugged:
            speak("Alert: Battery is fully charged. You can disconnect from the power source.")
            print("Alert: Battery is fully charged. You can disconnect from the power source.")
        else:
            speak("Battery level is normal.")
            print("Battery level is normal.")

    except Exception as e:
        print("An error occurred while checking battery status:" + str(e))
# Check the power consumption for the past 1 hour and display the app name which has consumed the most

# Define a function to open WhatsApp web
def open_whatsapp():
    
    # Define the path to the WhatsApp desktop executable
    whatsapp_executable_path = r"C:\\Program Files\WindowsApps\\5319275A.WhatsAppDesktop_2.2423.7.0_x64__cv1g1gvanyjgm\\WhatsApp.exe"  # Replace with the actual path

    # Check if the WhatsApp desktop executable exists
    if os.path.exists(whatsapp_executable_path):
        try:
            subprocess.Popen([whatsapp_executable_path])
            print("WhatsApp opened successfully.")
        except Exception as e:
            print("An error occurred while opening WhatsApp desktop app:", str(e))
    else:
        # If the desktop app doesn't exist, open the web version
        # Inform the user that WhatsApp Web is being opened
        print("Opening WhatsApp Web")

        # Open the WhatsApp Web URL in the default web browser
        webbrowser.open("https://web.whatsapp.com/")


# Define a function to open Gmail in the web browser
def open_gmail():
    # Open the Gmail URL in the default web browser
    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

    # Return a spoken message to confirm that Gmail is being opened
    return speak("Opening Gmail...")


# Define a function to temporarily stop listening to commands
def stop_listening():
    try:
        # Ask the user for the duration to stop listening
        speak("For how many seconds do you want to stop listening to commands?")
        stop_duration = takeCommand()

        # Check if a valid duration was provided and it's greater than 0 seconds
        if stop_duration is not None and int(stop_duration) > 0:
            # Inform the user that listening is paused for the specified duration
            speak(f"Stopped listening for {stop_duration} seconds.")
            time.sleep(int(stop_duration))

            # Inform the user that listening has resumed
            return speak(f"Listening resumed. You can continue your operations now.")
        else:
            # Inform the user that the duration provided is invalid, and listening continues
            return speak("Invalid duration. Listening continues.")
    except ValueError:
        # Handle cases where an invalid input (non-integer) is provided, and listening continues
        return speak("Invalid input. Listening continues.")


# Define a function to locate a location on Google Maps based on a query
def locate_location(query):
    # Define keywords that trigger location search
    keywords = ["where is", "locate"]

    # Check if any of the keywords are in the query
    for keyword in keywords:
        if keyword in query:
            # Extract the location from the query
            location = query.replace(keyword, "").strip()
            if location:
                # Format the location for the URL and construct the Google Maps URL
                location = "+".join(location.split())
                map_url = f"https://www.google.com/maps/search/?q={location}"

                # Open the Google Maps URL in the default web browser
                webbrowser.open(map_url)

                # Return a spoken message indicating the location is being located
                return speak(f"Locating {location.replace('+', ' ')}")

    # Return a message if the query didn't match any keywords
    return "Sorry, I couldn't understand the location you're looking for."


def capture_screenshot(file_path):
    try:
        # Capture the screenshot of the entire screen
        screenshot = ImageGrab.grab()

        # Save the screenshot to the specified file path
        screenshot.save(file_path)

        print(f"Screenshot saved to {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        

# Define a function to hibernate the computer
def hibernate():
    # Get the current operating system (Windows, Linux, or macOS)
    system_platform = platform.system()

    # Check the operating system and execute the appropriate hibernate command
    if system_platform == "Windows":
        # For Windows, use "rundll32.exe" to set the system to hibernate
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
    elif system_platform == "Linux":
        # For Linux, use "systemctl" to suspend the system
        subprocess.run(["systemctl", "suspend"], check=True)
    elif system_platform == "Darwin":
        # For macOS, use "pmset" to put the system to sleep (hibernation is not common on macOS)
        subprocess.run(["pmset", "sleepnow"], check=True)
    else:
        # Print a message for unsupported operating systems
        print("Unsupported operating system")
        
        
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def youtube_music():
    song_name = print("Enter the name of the song you want to play: ")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    
    # Set implicit wait time to handle dynamic page elements
    driver.implicitly_wait(10)
    
    # Navigate to YouTube
    driver.get('https://youtube.com')
    driver.maximize_window()
    
    # Locate the search input element and input the song name
    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "search_query")))
    search_input.send_keys(song_name)
    search_input.send_keys(Keys.RETURN)  # Submit the search query
    
    # Wait for search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'contents')))
    
    # Click the first video in the search results
    first_video = driver.find_element(By.CSS_SELECTOR, '#contents ytd-video-renderer')
    first_video.click()
    
    # Wait for the video to play - You may adjust the duration as needed
    time.sleep(420)  # This waits for 30 seconds, you can change it based on the length of the video
    
    # Close the browser
    driver.quit()


# Define a function to shut down the computer
def shutdown():
    # Get the current operating system (Windows, Linux, or macOS)
    system_platform = platform.system()

    # Check the operating system and execute the appropriate shutdown command
    if system_platform == "Windows":
        # For Windows, use "shutdown" command with "/s" to initiate a shutdown immediately
        subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
    elif system_platform == "Linux" or system_platform == "Darwin":
        # For Linux and macOS, use "shutdown" with "-h" to halt the system immediately
        subprocess.run(["shutdown", "-h", "now"], check=True)
    else:
        # Print a message for unsupported operating systems
        print("Unsupported operating system")

# Define a function to restart the computer
def restart():
    # Get the current operating system (Windows, Linux, or macOS)
    system_platform = platform.system()

    # Check the operating system and execute the appropriate restart command
    if system_platform == "Windows":
        # For Windows, use "shutdown" command with "/r" to restart immediately
        subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
    elif system_platform == "Linux" or system_platform == "Darwin":
        # For Linux and macOS, use "reboot" to initiate a system reboot
        subprocess.run(["reboot"], check=True)
    else:
        # Print a message for unsupported operating systems
        print("Unsupported operating system")


# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')  # Initialize the text-to-speech engine using the 'sapi5' backend
voices = engine.getProperty('voices')  # Get the list of available voices from the engine
engine.setProperty('voice', voices[1].id)  # Set the voice for the engine to use (in this case, using the first voice in the list)


# Define a custom exception for speech-related errors
class SpeechError(Exception):
    pass

#Text-to-speech engine to convert the input 'audio' into spoken words
def speak(audio):   # Function to handle speech output
    try:
        engine.say(audio)  # Provide the text to the engine to be spoken
        engine.runAndWait()  # Block execution until the speech is finished
        pass
    except Exception as e:
        # Handle any exceptions related to speech here
        raise SpeechError("Speech error: " + str(e))

# Personalization: Allow users to provide their name
def set_personalization():
    '''speak("Hello! This is your personal voice-controlled virtual assistant. Please tell me your good name for future communications.")'''
    speak("Hello. This is Jarvis. Please tell me your good name for future communications.")
    while True:
        user_name = takeCommand()  # Capture the user's spoken response as text
        print(f"User said: {user_name}")  # Debug print

        # Confirm the user's name
        speak(f"{user_name}. Is that correct? Please say 'yes' or 'no'.")  # Speak the user's name and ask for confirmation

        confirmation = takeCommand().lower()  # Capture the user's confirmation response as text and convert to lowercase
        print(f"User confirmed: {confirmation}")  # Debug print

        if 'yes' in confirmation:  # Check if the user confirmed their name
            speak(f"Thank you, {user_name}! I'll remember that.")  # Speak a confirmation message with the user's name
            return user_name  # Return the user's name as the result of the function
        elif 'no' in confirmation:  # Check if the user indicated that the name is incorrect
            speak("I'm sorry for the misunderstanding. Please tell me your name again.")  # Speak a message asking the user to provide their name again
        else:
            speak("I didn't understand your response. Please say your name again.")  # Speak a message indicating that the response was not understood and prompt the user to provide their name again


# Function to take voice input from the user
def takeCommand():
    # It takes microphone input from the user and returns string output

    # Create a Recognizer instance for audio recognition
    r = sr.Recognizer()

    # Use the system's default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")  # Indicate that the assistant is listening
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        r.pause_threshold = 1  # Set the pause threshold for recognizing the end of speech; Lower the threshold for faster response
        #r.non_speaking_duration = 0.2  # Adjust as needed
        audio = r.listen(source)  # Capture audio from the microphone  #timeout=30

    try:
        print("Recognizing...")  # Indicate that the assistant is recognizing the audio
        query = r.recognize_google(audio, language='en-in')  # Use Google Web Speech API for recognition
        print(f"User : {query}\n")  # Print the recognized user input

    except sr.UnknownValueError:
        print("Sorry, couldn't understand your speech.")
        return ""
    except sr.RequestError:
        print("There was an issue with the speech recognition service.")
        return ""
    except Exception as e:
        # If an exception occurs during recognition
        # Print a message asking the user to repeat the command
        print("Unable to Recognize your voice.")
        print("Please repeat your command...")
        return "None"  # Return "None" to indicate that recognition was unsuccessful

    return query  # Return the recognized user input


# Define a function to send an email based on voice input
def SendEmail():

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    # Set up the microphone as the audio source
    with sr.Microphone() as source:
        print('Clearing background noise...')
        
        # Adjust for ambient noise to improve speech recognition
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print('Listening....')
        
        # Capture audio input
        recordaudio = recognizer.listen(source)
        print('Recognizing...')

    try:
        print('Printing the message...')
        
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(recordaudio, language='en-US')
        print('Your message: {}'.format(text))

        # Set email receiver address
        recevier = 'aaravrshah811@gmail.com'
        # Use the recognized text as the email message
        message = text
        # Set up the email sender with Gmail credentials
        sender = yagmail.SMTP('shaharav606@gmail.com', 'zyjfkkyxaiblemuz')
        
        # Send the email with the recognized text as the content
        sender.send(to=recevier, subject='This is mail generated by voicegpt', contents=message)

    except Exception as ex:
        print(ex)
        speak("Sorry sir or mam. I am not able to send this email")
        
# Function to extract an email address from text

# Function to translate text using Google Translate
def translate_text(text, target_language):
    # Create a translator object from the Googletrans library
    translator = Translator()

    # Translate the input text to the specified target language
    translated_text = translator.translate(text, dest=target_language)

    # Return the translated text extracted from the translation object
    return translated_text.text

# Define a dictionary to map spoken language names to their language codes
LANGUAGE_MAPPING = {
        'english': 'en',
        'spanish': 'es',
        'french': 'fr',
        'hindi': 'hi',
        # Add more language mappings as needed
}

# Function to greet the user based on the time of the day and personalized title/name
def wishMe(user_name):
    hour = int(datetime.datetime.now().hour)   # Get the current hour of the day as an integer

    # Define a dictionary with different greetings for each time of the day
    greetings = {
        'morning': [
            # List of morning greetings with placeholders for the user's name
            f"Good morning, {user_name}! Have a productive day ahead.",
            f"It's time to rise and shine, {user_name}! Take a deep breath, put on a smile, and get ready to toe the line!",
            f"A brand new day has begun, {user_name}! Embrace the opportunities it brings.",
            f"Hello {user_name}! Yesterday is miles away, and today is a new today. With new goals to meet, let's rise up and jump to our feet.",
            f"The day has yet to be written, but there are several ways to fill the page; it's up to you to write your own story. A very good morning {user_name}!",
            f"The day is a blank canvas yet to be painted with the colors of life. Seize the day {user_name}!",
        ],
        'afternoon': [
            # List of afternoon greetings with placeholders for the user's name
            f"Good Afternoon {user_name}!",
            f"Hello {user_name}! Your dream doesn't have an expiration date. Take a deep breath and try again this afternoon.",
            f"The biggest motivation is your own thoughts, so think big and motivate yourself to win. Good Afternoon {user_name}!",
        ],
        'evening': [
            # List of morning greetings with placeholders for the user's name
            f"Good Evening! {user_name}",
            f"Every sunset brings the promise of a new dawn. Happy Evening {user_name}",
            f"Sunsets are proof that no matter what happens, every day can end beautifully. Enjoy each moment {user_name}",
            f"Do not count the days, make the days count. Good evening {user_name}!"
        ]
    }

    # Translate the greetings based on the output_language
    translated_greetings = {
        key: [translate_text(greeting.format(user_name=user_name), target_language=preferred_language) for greeting in value]
        for key, value in greetings.items()
    }

    if 0 <= hour < 12:
        time_of_day = 'morning'
    elif 12 <= hour < 18:
        time_of_day = 'afternoon'
    else:
        time_of_day = 'evening'

    user_greetings = translated_greetings[time_of_day]  # Get the list of greetings corresponding to the current time of day
    random_greeting = random.choice(user_greetings)  # Choose a random greeting from the list

    return random_greeting  # Return the personalized greeting


# Function to set the preferred language based on user input
def set_preferred_language():
    speak("Please select your preferred language for conversation (e.g., English, Spanish, French, Hindi): ")
    while True:
        spoken_language = takeCommand().lower()  # Capture the user's spoken language choice and convert to lowercase

        # Check if the spoken language is in the LANGUAGE_MAPPING dictionary
        if spoken_language in LANGUAGE_MAPPING:
            preferred_language = LANGUAGE_MAPPING[spoken_language]  # Get the language code
            speak(f"Preferred language set to {spoken_language}.")
            return preferred_language  # Return the selected language code
        else:
            speak("Sorry, that language is not supported. Please choose a supported language.")
            
def latest_news():
    try:
        # URL of the Google News RSS feed
        news_url = "https://news.google.com/news/rss"

        # Open the URL and read the XML data
        with urllib.request.urlopen(news_url) as Client:
            xml_page = Client.read()

        # Close the URL connection
        Client.close()

        # Parse the XML data using BeautifulSoup
        soup_page = BeautifulSoup(xml_page, "xml")

        # Find all news items
        news_list = soup_page.findAll("item")

        # Display the top 15 news headlines
        for news in news_list[:15]:
            headline = news.title.text.encode('utf-8').decode('utf-8')  # Convert to UTF-8 encoding and decode
            print(headline)

    except Exception as e:
        print(e)

'''
def visualize_data(x, y, x_label, y_label, title, chart_type='bar'):
    """
    Visualize data using Matplotlib.

    Parameters:
    - x: List of data labels or categories
    - y: List of data values
    - x_label: Label for the x-axis
    - y_label: Label for the y-axis
    - title: Title for the chart
    - chart_type: Type of chart (e.g., 'bar', 'line', 'scatter', etc.)

    Returns:
    - None (displays the chart)
    """
    if chart_type == 'bar':
        plt.bar(x, y)
    elif chart_type == 'line':
        plt.plot(x, y)
    elif chart_type == 'scatter':
        plt.scatter(x, y)
    else:
        raise ValueError("Unsupported chart type")

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

# Example usage:
categories = ['Category A', 'Category B', 'Category C', 'Category D']
data = [10, 20, 15, 25]

visualize_data(categories, data, 'Categories', 'Data Values', 'Data Visualization Example', chart_type='bar')
'''

if __name__== "__main__":
    user_name = set_personalization()  # Ask the user for their name and store it in the user_name variable

    preferred_language = set_preferred_language()  # Set the preferred language based on user input

    # Supported languages
    SUPPORTED_LANGUAGES = list(LANGUAGE_MAPPING.values())  # Get the language codes from the LANGUAGE_MAPPING dictionary

    if preferred_language not in SUPPORTED_LANGUAGES:
        speak("Preferred language not supported. Using English as default.")
        preferred_language = 'en'
    # else:
    # speak("Language preference set successfully.")

    greeting = wishMe(user_name)
    speak(greeting)
    speak("Feel free to ask for any help.")  # Speak a prompt for the user to ask for help

    while True:
        query = takeCommand().lower()  # Directly retrieve the recognized transcript

        if 'organised files' in query:
            organize_files()

        elif 'move file' in query:
            speak("Please provide the source file path.")
            source_path = takeCommand()
            speak("Please provide the destination folder path.")
            destination_path = takeCommand()
            move_file(source_path, destination_path)

        elif 'copy file' in query:
            speak("Please provide the source file path.")
            source_path = takeCommand()
            speak("Please provide the destination folder path.")
            destination_path = takeCommand()
            copy_file(source_path, destination_path)

        elif 'rename file' in query:
            speak("Please provide the current name of the file.")
            old_name = takeCommand()
            speak("Please provide the new name for the file.")
            new_name = takeCommand()
            rename_file(old_name, new_name)
            
        elif 'news' in query:
            speak("Please take the url")
            latest_news()

       # play YouTube song
        elif 'song' in query or 'music' in query:
            speak("Enter the name of the song you want to play: ")
            song_name = takeCommand()
            youtube_music(song_name)
            
            
        elif 'compress file' in query:
            speak("Please provide the folder path.")
            folder_path = takeCommand()
            speak("Please provide the file name.")
            file_name = takeCommand()

            found_path = search_file_in_folder(folder_path, file_name)

            if found_path:
                print(f"File '{file_name}' found at: {found_path}")
                compress_file(found_path)
                print(f"File '{file_name}' compressed.")
                speak(f"File '{file_name}' found and compressed successfully.")
            else:
                print(f"File '{file_name}' not found in the specified folder.")
                speak(f"File '{file_name}' not found in the specified folder.")

        elif 'open folder' in query:
            speak("Sure, please provide the folder name.")
            folder_name = takeCommand().lower()
            open_folder(folder_name)

        elif 'convert file' in query:
            speak("Please provide the source file path.")
            source_path = takeCommand()
            speak("Please provide the destination file path (including the desired format extension).")
            destination_path = takeCommand()
            speak("Please specify the desired format (PDF, JPEG, PNG, TXT, MP3, etc.).")
            new_format = takeCommand().upper()

            convert_file_format(source_path, destination_path, new_format)

        elif 'compress file' in query:
            speak("Please provide the folder path.")
            folder_path = takeCommand()
            speak("Please provide the file name.")
            file_name = takeCommand()

            found_path = search_file_in_folder(folder_path, file_name)

            if found_path:
                print(f"File '{file_name}' found at: {found_path}")
                compress_file(found_path)
                print(f"File '{file_name}' compressed.")
                speak(f"File '{file_name}' found and compressed successfully.")
            else:
                print(f"File '{file_name}' not found in the specified folder.")
                speak(f"File '{file_name}' not found in the specified folder.")

            
        # elif 'email_extract' in query:
        #     print("Please speak your email address:")
        #     email = takeCommand()
        #     # Check if the recognized text contains an email address
        #     email = email.replace(" at the rate ", "@")  # Replace " at the rate " with "@"
        #     extracted_email = extract_email(email)
        #     if extracted_email:
        #         print(f"Final extracted email address: {extracted_email}")

        elif 'email' in query:
            SendEmail()
            
        elif 'screenshot' in query:
            file_path = "screenshot.png"  # Change this to your desired file path
            capture_screenshot(file_path)

        elif "change brightness to" in query:
            query = query.replace("change brightness to", "")
            try:
                # Check if the percentage symbol (%) is present
                if "%" in query:
                    brightness_percentage = int(query.strip("%").strip())
                else:
                    brightness_percentage = int(query.strip())

                if 0 <= brightness_percentage <= 100:
                    changeBrightness(brightness_percentage)
                else:
                    speak("Invalid brightness value. Please specify a percentage between 0 and 100.")
            except ValueError:
                speak("Invalid brightness value. Please specify a valid percentage.")

        elif "increase brightness" in query:    #error in function
            increaseBrightness()

        elif "decrease brightness" in query:
            decreaseBrightness()

        elif 'open website' in query:
            speak("Sure, please provide the website URL.")
            website_url = takeCommand()  # Directly retrieve the recognized URL
            webbrowser.open(website_url)
            speak(f"Opening {website_url}")

        # Logic for executing tasks based on query
        elif 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'troubleshoot system' in query:
            speak("Running system troubleshooting. Please wait.")
            troubleshoot_system()

        elif 'battery status' in query:
            check_battery_status()

        elif 'system specifications' in query:
            cpu_info, ram_info, disk_info = get_system_specifications()

            speak("Checking system specifications...")
            speak("Here are your system specifications, printed on the screen.")
            print("CPU Information:")
            for key, value in cpu_info.items():
                print(key, value)

            speak("RAM Information:")
            for key, value in ram_info.items():
                print(key, value)

            speak("Storage Information:")
            for key, value in disk_info.items():
                print(key, value)

            troubleshoot_system()

        elif 'open whatsapp' in query:
            open_whatsapp()

        elif "who made you" in query or "who created you" in query:
            speak("I have been created by Aarav Kumar Shah, Sahil Shah, Utsav Bhavsar, Manav Raval and Madhav Mehta under the supervision of faculty Dr. Rutvij Jhaveri Sir.")

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif "open gmail" in query or "open mail" in query:
            open_gmail()

        elif "don't listen" in query or "wait a second" in query or "stop listening" in query:
            stop_listening()

        elif "where is" in query or "locate" in query:
            locate_location(query)

        elif "take selfie" in query or "take a photo" in query or "take picture" in query:
            speak("Say Cheese...!")
            ec.capture(0, "Camera ", "img.jpg")

        elif "i love you" in query:
            speak("It's hard to understand")

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            hibernate()

        elif 'shutdown' in query:
            speak("Please save your work and close any running applications.")
            response = takeCommand().lower()

            if "ok" in response or "doesn't matter" in response or "sure" in response or "go ahead" in response:
                speak("Shutting down the system...")
                shutdown()

        elif 'restart' in query:
            speak("Please save your work and close any running applications.")
            response = takeCommand().lower()

            if "ok" in response or "doesn't matter" in response or "sure" in response or "go ahead" in response:
                speak("Restarting the system...")
                shutdown()

        elif 'exit' in query:
            speak(f"Thankyou...Have a good day ahead {user_name}.")
            break
        else:
            print("No query matched.Please try again.")
'''Additional features to be added:

Reminders and Alarms: Allow the user to set reminders or alarms by specifying a time and task.
 The assistant can then notify the user when the time comes.
 
 
      elif 'compress file' in query:
            speak("Please provide the source file path.")
            source_path = takeCommand()
            speak("Please provide the destination path for the compressed ZIP archive.")
            destination_path = takeCommand()
            compress_to_zip(source_path, destination_path)
            
            
 
# Additional feature: Reminders and Alarms
# You can integrate this feature by adding a function that allows users to set alarms.
# When the time for an alarm comes, the assistant can notify the user.
def set_alarm():
    speak("Sure, when would you like to set the alarm for?")
    alarm_time = takeCommand()
    # Parse the user's input to extract the alarm time
    # Schedule a task to notify the user at the specified time

# Additional feature: Calendar Integration
# Integrate with the user's calendar to schedule appointments, meetings, or events based on voice commands.
def schedule_event():
    speak("What event would you like to schedule?")
    event_details = takeCommand()
    # Integrate with a calendar API to create the event
    
        elif 'remind me' in query:
            set_alarm()

        elif 'take a note' in query:
            take_note()

        elif 'schedule event' in query:
            schedule_event()


def translate_document(language):
    # Use translation APIs to convert document content to the desired language and read it aloud
    pass
 
 from pyvoiceprint import VoiceAuth

def authenticate_user():
    voice_auth = VoiceAuth()
    enrolled_users = voice_auth.get_enrolled_users()
    if not enrolled_users:
        print("No enrolled users found.")
        return

    user_input = recognize_speech()
    authenticated_user = voice_auth.authenticate(user_input)
    if authenticated_user:
        print("User authenticated.")
    else:
        print("Authentication failed.")

 
 Multi-Language Support: Enable the virtual assistant to understand and respond to voice commands in multiple languages, enhancing its accessibility and usability for users from diverse linguistic backgrounds.
 
 Voiceprint Authentication: Integrate voiceprint authentication for added security, allowing the virtual assistant to identify and authenticate users based on their unique voice characteristics.
 
 
 
 Language Support: Extend the assistant's language capabilities to understand and respond in multiple languages, allowing users from different regions to interact with it.
 
 def search_web(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

 
 Folder Organization: Allow users to provide criteria for organizing files within a folder. The assistant can sort files based on criteria such as file type, creation date, or even user-defined tags.
 
 Startup Manager: Help users manage startup programs and services to improve boot times and system responsiveness.
 
Secure Authentication: Improve the email functionality by using modern authentication methods, such as OAuth 2.0, instead of directly using email and password.
Email Management: Allow users to read, compose, and manage emails using voice commands. The assistant can also help organize emails into folders and respond to messages.

Logging: Implement logging mechanisms to keep track of assistant interactions and potential issues for debugging and analysis.

Real-time Weather - storing info in file...use buffering...automation


        elif 'play music' in query:
            music_dir = ''    #D:\\Non Critical\\songs\\Favorite Songs2
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

Exit and Shutdown Commands: Implement voice commands to gracefully exit the assistant or shut down the system.

Music Streaming: Instead of playing locally stored music, you could integrate with online music streaming services to play music on user request.

Voice Commands Customization: Allow users to define their own custom voice commands for specific actions they frequently perform.

Voice Commands History: Allow users to review their recent voice commands and interactions.  : log file
'''

"""
Fitness and Health Tracking: Create a feature that helps users track their fitness and health goals, setting goals and automating the report generation.
"""

"""
Social Media Integration: Allow users to post updates or tweets on their social media accounts using voice commands.

import tweepy
from instabot import Bot
from linkedin import linkedin

# Twitter API credentials
twitter_consumer_key = "your_consumer_key"
twitter_consumer_secret = "your_consumer_secret"
twitter_access_token = "your_access_token"
twitter_access_token_secret = "your_access_token_secret"

# Instagram credentials
instagram_username = "your_instagram_username"
instagram_password = "your_instagram_password"

# LinkedIn credentials
linkedin_access_token = "your_linkedin_access_token"

# Initialize Twitter API
twitter_auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
twitter_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(twitter_auth)

# Initialize Instagram API
instagram_bot = Bot()
instagram_bot.login(username=instagram_username, password=instagram_password)

# Initialize LinkedIn API
linkedin_auth = linkedin.LinkedInDeveloperAuthentication(
    "your_linkedin_consumer_key",
    "your_linkedin_consumer_secret",
    "your_linkedin_user_token",
    "your_linkedin_user_secret",
    "http://localhost:8000",
    linkedin.PERMISSIONS.enums.values()
)
linkedin_api = linkedin.LinkedInApplication(authentication=linkedin_auth)

def post_tweet(text):
    try:
        twitter_api.update_status(text)
        print("Tweet posted successfully!")
    except tweepy.TweepError as e:
        print("Error posting tweet:", e)

def post_instagram_update(caption, image_path):
    try:
        instagram_bot.upload_photo(image_path, caption=caption)
        print("Instagram update posted successfully!")
    except Exception as e:
        print("Error posting Instagram update:", e)

def post_linkedin_update(text):
    try:
        linkedin_api.submit_share(text)
        print("LinkedIn update posted successfully!")
    except Exception as e:
        print("Error posting LinkedIn update:", e)

def main():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            platform = input("Enter the social media platform (twitter/instagram/linkedin): ").lower()

            if platform == "twitter":
                post_tweet(text)
            elif platform == "instagram":
                caption = input("Enter the Instagram caption: ")
                image_path = input("Enter the path to the image: ")
                post_instagram_update(caption, image_path)
            elif platform == "linkedin":
                post_linkedin_update(text)
            else:
                print("Invalid platform.")

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; check your network connection.", e)

if _name_ == "_main_":
    main()

"""

