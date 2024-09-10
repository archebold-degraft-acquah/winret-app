import pyperclip
import keyboard
import pyttsx3
import time
import requests
import wx
import subprocess
import os


# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Set up wx for error handling and UI display
app = wx.App(False)

# Function to fetch definition from dictionary API
def fetch_definition(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()

        # Extract the definition from the response
        if data and isinstance(data, list):
            meanings = data[0].get('meanings', [])
            if meanings:
                definitions = meanings[0].get('definitions', [])
                if definitions:
                    return definitions[0].get('definition', 'Definition not found.')
        return "Definition not found."
    except requests.exceptions.RequestException as e:
        wx.MessageBox(f"Error fetching definition: {e}", "Error", wx.OK | wx.ICON_ERROR)
        return None

# Function to announce the word definition using TTS
def announce_definition():
    word = pyperclip.paste().strip()  # Get word from clipboard
    if word:
        definition = fetch_definition(word)
        if definition:
            tts_engine.say(f"The definition of {word} is: {definition}")
            tts_engine.runAndWait()
    else:
        wx.MessageBox("No word found in clipboard", "Error", wx.OK | wx.ICON_ERROR)

# Function to check for double press within 1 second
def detect_key_press():
    first_press_time = time.time()
    while True:
        if keyboard.is_pressed('ctrl+alt+['):
            second_press_time = time.time()
            if second_press_time - first_press_time <= 1:  # Check if second press is within 1 second
                announce_definition()
                break
            else:
                first_press_time = second_press_time  # Reset if timing fails
        time.sleep(0.1)

# Main loop to listen for the double key press
def start_key_detection():
#    tts_engine.say(f"WinretApp {current_version} is running...")
#    tts_engine.runAndWait()
    while True:
        if keyboard.is_pressed('ctrl+alt+['):
            detect_key_press()
        time.sleep(0.1)

