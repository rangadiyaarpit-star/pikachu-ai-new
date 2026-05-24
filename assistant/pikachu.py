from datetime import datetime
import speech_recognition as sr
import pyttsx3
import subprocess
import re
from assistant.brain import detect_intent
from assistant.memory import remember, recall
from assistant.ai import ask_ai
# =========================================
# SPEECH RECOGNITION
# =========================================

recognizer = sr.Recognizer()




# =========================================
# VOICE ENGINE
# =========================================

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 150)

engine.setProperty('volume', 1.0)

# =========================================
# CLEAN TEXT
# =========================================

def clean_text(text):

    text = re.sub(r'[^\w\s,.!?]', '', text)

    return text

# =========================================
# SPEAK FUNCTION
# =========================================

def speak(text):

    try:

        text = clean_text(text)

        print("Pikachu:", text)

        engine = pyttsx3.init()

        voices = engine.getProperty('voices')

        engine.setProperty('voice', voices[0].id)

        engine.setProperty('rate', 170)

        engine.setProperty('volume', 1)

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:

        print("Speak Error:", e)

            
            
# =========================================
# LISTEN FUNCTION
# =========================================

def listen():

    try:

        with sr.Microphone(device_index=2) as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            print("Recognizing...")

            command = recognizer.recognize_google(audio)

            command = command.lower().strip()

            print("You Said:", command)

            return command

    except sr.UnknownValueError:

        speak("I don't understand")

        return ""

    except sr.WaitTimeoutError:

        print("Listening timeout")

        return ""

    except Exception as e:

        print("Error:", e)

        return ""

# =========================================
# ADB PATH
# =========================================

ADB = r"platform-tools\adb.exe"

# =========================================
# ADB COMMAND FUNCTION
# =========================================

def adb(command):

    full_command = f'{ADB} {command}'

    print(full_command)

    subprocess.run(full_command, shell=True)


# =========================================
# MOBILE COMMANDS
# =========================================
def pause_listener():

    stream.stop_stream()

def resume_listener():

    stream.start_stream()   
def process_command(c):
    c = c.lower().strip()
    intent = detect_intent(c)

    # =========================================
    # OPEN APPS
    # =========================================
    if "pikachu" in c:

        stream.stop_stream()

        speak("Yes")

        stream.start_stream()

        return
        # =========================================
    # MEMORY SAVE
    # =========================================

    if intent == "memory_save":

        text = c.replace("remember", "").strip()

        if " is " in text:

            key, value = text.split(" is ", 1)

            remember(key.strip(), value.strip())

            return f"I will remember that {key} is {value}"
          
        else:

            return "Tell me in format remember something is something"
        
    elif "open settings" in c:

        speak("Opening settings")

        adb(
            'shell am start -a android.settings.SETTINGS'
        )
        return "## ⚙️ Opening Settings"

    elif "wi-fi on" in c:

        speak("Turning WiFi on")

        adb("shell svc wifi enable")
        return "## 📶 Turning WiFi On"

    elif "wi-fi off" in c:

        speak("Turning WiFi off")

        adb("shell svc wifi disable")
        return "## 📶 Turning WiFi Off"

    elif "bluetooth on" in c:

        speak("Turning Bluetooth on")

        adb("shell svc bluetooth enable")
        return "## 📶 Turning Bluetooth On"


    elif "bluetooth off" in c:

        speak("Turning Bluetooth off")

        adb("shell svc bluetooth disable")
        return "## 📶 Turning Bluetooth Off"
        
    elif "open camera" in c:

        speak("Opening Camera")

        adb(
            'shell am start -a android.media.action.IMAGE_CAPTURE'
        )
        return "## 📷 Opening Camera"
    elif c.startswith("play"):

        query = (
            c.replace("play", "")
            .replace("song", "")
            .replace("video", "")
            .strip()
        )

        if query:

            speak(f"Playing {query}")

            # Open YouTube search
            query_url = query.replace(" ", "+")

            adb(
                f'shell am start -a android.intent.action.VIEW '
                f'-d "https://www.youtube.com/results?search_query={query_url}"'
            )

            # Wait for YouTube to open
            import time

            time.sleep(5)

            # Tap first video
            adb("shell input tap 500 350")
            return "## 🎬 Playing Video"
        else:

            speak("What should I play")
           
    elif "search" in c:

        query = c.replace("search", "").strip()

        if query:

            speak(f"Searching {query}")

            query_url = query.replace(" ", "+")

            adb(
                f'shell am start -a android.intent.action.VIEW '
                f'-d "https://www.google.com/search?q={query_url}"'
            )
            return "## 🔍 Searching"
        else:

            speak("What should I search")  
    elif "hi" in c:

        speak("Hello")
        return "## 👋 Hello"

    elif "how are you" in c:

        speak("I am fine")
        return "## 🤗 I am fine"

    elif "your name" in c:

        speak("I am Pikachu") 
        return "## ⚡ I am Pikachu"      
    elif "open" in c:

        app_name = c.replace("open", "").strip()

        apps = {

            "youtube": "com.google.android.youtube",
            "whatsapp": "com.whatsapp",
            "chrome": "com.android.chrome",
            "instagram": "com.instagram.android",
            "telegram": "org.telegram.messenger",
            "facebook": "com.facebook.katana",
            "camera": "com.android.camera",
            "settings": "com.android.settings",
            "setting": "com.android.settings",
            "playstore": "com.android.vending",
            "play store": "com.android.vending"

        }

        if app_name in apps:

            speak(f"Opening {app_name}")

            adb(
                f'shell monkey -p {apps[app_name]} '
                f'-c android.intent.category.LAUNCHER 1'
            )
            return f"## 📱 Opening {app_name}"
        else:

            speak("Application not found")        
    # =========================================
    # MOBILE NAVIGATION
    # =========================================
    elif "message bar" in c:

        speak("Opening message bar")

        adb("shell input swipe 500 0 500 1000")
        return "## 📱 Opening Message Bar"
    elif "home" in c:

        speak("Going Home")

        adb("shell input keyevent 3")
        return "## 📱 Going Home"

    elif "back" in c:

        speak("Going Back")

        adb("shell input keyevent 4")
        return "## 📱 Going Back"

    elif "recent apps" in c:

        speak("Opening Recent Apps")

        adb("shell input keyevent 187")
        return "## 📱 Opening Recent Apps"

    # =========================================
    # VOLUME CONTROL
    # =========================================

    elif "volume up" in c:

        speak("Increasing volume")

        adb("shell input keyevent 24")
        return "## 🔊 Increasing Volume"
    elif "volume down" in c:

        speak("Decreasing volume")

        adb("shell input keyevent 25")
        return "## 🔊 Decreasing Volume"

    elif "mute" in c:

        speak("Muting volume")

        adb("shell input keyevent 164")
        return "## 🔊 Muting Volume"

    # =========================================
    # SCREEN CONTROL
    # =========================================

    elif "swipe up" in c:

        speak("Swiping up")

        adb("shell input swipe 500 1500 500 500")
        return "## 🖼️ Swiping Up"

    elif "swipe down" in c:

        speak("Swiping down")

        adb("shell input swipe 500 500 500 1500")
        return "## 🖼️ Swiping Down"

    elif "swipe left" in c:

        speak("Swiping left")

        adb("shell input swipe 1000 500 100 500")
        return "## 🖼️ Swiping Left"

    elif "swipe right" in c:

        speak("Swiping right")

        adb("shell input swipe 100 500 1000 500")
        return "## 🖼️ Swiping Right"

    elif "tap" in c:

        speak("Tapping screen")

        adb("shell input tap 500 500")
        return "## 🖼️ Tapping Screen"

    # =========================================
    # POWER CONTROL
    # =========================================

    elif "lock phone" in c:

        speak("Locking phone")

        adb("shell input keyevent 26")
        return "## 📱 Locking Phone"

    elif "unlock phone" in c:

        speak("Unlocking phone")

        adb("shell input swipe 300 1000 300 300")
        return "## 📱 Unlocking Phone"

    # =========================================
    # FLASHLIGHT
    # =========================================

    elif "flashlight on" in c:

        speak("Turning flashlight on")

        adb("shell cmd flashlight set 1")
        return "## 📷 Turning Flashlight On"


    elif "flashlight off" in c:

        speak("Turning flashlight off")

        adb("shell input keyevent 26")
        return "## 📷 Turning Flashlight Off"

    # =========================================
    # SCREENSHOT
    # =========================================

    elif "take screenshot" in c:

        speak("Taking screenshot")

        adb("shell screencap /sdcard/pikachu.png")
        return "## 📷 Taking Screenshot"

    # =========================================
    # TYPE MESSAGE
    # =========================================

    elif "type hello" in c:

        speak("Typing hello")

        adb('shell input text "Hello_From_Pikachu"')
        return "## ⌨️ Typing Hello"

    # =========================================
    # TIME
    # =========================================

    elif "time" in c:

                current_time = datetime.now().strftime("%I:%M %p")

                speak(f"The time is {current_time}")

                return f"""

            # ⌚ Current Time

            ## 🕒 {current_time}

            ---

            ✅ Time fetched successfully

            """

    # =========================================
    # EXIT
    # =========================================

    elif "exit" in c or "stop" in c:

        speak("Goodbye")
        return "## 👋 Goodbye"
        exit()
        
        # =========================================
    # MEMORY RECALL
    # =========================================

    elif intent == "memory_recall":

        key = c.replace("what is", "").strip()

        value = recall(key)

        if value:

            return f"{key} is {value}"

        else:

            return "I don't remember that"
    # =========================================
    # UNKNOWN COMMAND
    # =========================================

    else:

        response = ask_ai(c)

        return response

