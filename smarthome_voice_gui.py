import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import os
import threading
import speech_recognition as sr
import pyttsx3
import re

# Helper to load icon images (use simple colored rectangles if no icon files)
def get_icon(color, size=(48, 48)):
    img = Image.new('RGBA', size, color)
    return ImageTk.PhotoImage(img)

DEVICE_INFO = {
    'Light': {'on': '#ffe066', 'off': '#dcdde1', 'synonyms': ['light', 'lamp']},
    'Fan': {'on': '#00a8ff', 'off': '#dcdde1', 'synonyms': ['fan']},
    'AC': {'on': '#7ed6df', 'off': '#dcdde1', 'synonyms': ['ac', 'air conditioner', 'air conditioning']},
    'Heater': {'on': '#e17055', 'off': '#dcdde1', 'synonyms': ['heater', 'heat']},
}

class DeviceCard(ttk.Frame):
    def __init__(self, master, name, icon_on, icon_off, *args, **kwargs):
        super().__init__(master, style='Card.TFrame', padding=10, *args, **kwargs)
        self.name = name
        self.icon_on = icon_on
        self.icon_off = icon_off
        self.state = False  # OFF by default
        self.icon_label = ttk.Label(self)
        self.icon_label.pack()
        self.name_label = ttk.Label(self, text=name, font=('Segoe UI', 14, 'bold'))
        self.name_label.pack(pady=(5, 0))
        self.state_label = ttk.Label(self, text='OFF', font=('Segoe UI', 12), foreground='#e84118')
        self.state_label.pack()
        self.update_ui()
        self.bind_widgets()

    def bind_widgets(self):
        for widget in (self, self.icon_label, self.name_label, self.state_label):
            widget.bind('<Button-1>', self.toggle)

    def toggle(self, event=None):
        self.state = not self.state
        self.update_ui()
        self.master.master.log(f'{self.name} turned {"ON" if self.state else "OFF"}')
        self.master.master.speak(f'{self.name} turned {"on" if self.state else "off"}')

    def set_state(self, on):
        self.state = on
        self.update_ui()
        self.master.master.log(f'{self.name} turned {"ON" if self.state else "OFF"}')
        self.master.master.speak(f'{self.name} turned {"on" if self.state else "off"}')

    def update_ui(self):
        icon = self.icon_on if self.state else self.icon_off
        self.icon_label.configure(image=icon)
        self.icon_label.image = icon
        self.state_label.configure(text='ON' if self.state else 'OFF',
                                   foreground='#44bd32' if self.state else '#e84118')

class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Smart Home Voice-Controlled System')
        self.geometry('800x500')
        self.configure(bg='#f5f6fa')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Card.TFrame', background='#fff', relief='raised', borderwidth=1)
        self.create_widgets()
        self.recognizer = sr.Recognizer()
        self.listening = False
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)

    def create_widgets(self):
        # Title
        title = ttk.Label(self, text='Smart Home Voice-Controlled System', font=('Segoe UI', 20, 'bold'))
        title.pack(pady=10)

        # Device frame (grid for modern look)
        self.device_frame = ttk.Frame(self)
        self.device_frame.pack(pady=20)
        self.devices = {}
        col = 0
        row = 0
        for i, (dev, colors) in enumerate(DEVICE_INFO.items()):
            icon_on = get_icon(colors['on'])
            icon_off = get_icon(colors['off'])
            card = DeviceCard(self.device_frame, dev, icon_on, icon_off)
            card.grid(row=row, column=col, padx=30, pady=10)
            self.devices[dev] = card
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Voice command button
        self.voice_btn = ttk.Button(self, text='🎤 Speak Command', command=self.on_voice_command)
        self.voice_btn.pack(pady=10)

        # Screenshot button
        self.screenshot_btn = ttk.Button(self, text='📸 Take Screenshot', command=self.take_screenshot)
        self.screenshot_btn.pack(pady=5)

        # Command log
        self.log_text = tk.Text(self, height=5, state='disabled', bg='#f0f0f0', font=('Segoe UI', 10))
        self.log_text.pack(fill='x', padx=20, pady=10)

    def on_voice_command(self):
        if self.listening:
            return
        self.listening = True
        self.voice_btn.config(text='🎤 Listening...')
        self.log('Listening for command...')
        threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            try:
                command = self.recognizer.recognize_google(audio)
                self.log(f'Heard: "{command}"')
                self.process_command(command)
            except sr.UnknownValueError:
                self.log('Sorry, could not understand the audio.')
                self.speak('Sorry, I could not understand the audio.')
            except sr.RequestError:
                self.log('Could not request results from speech recognition service.')
                self.speak('Speech recognition service error.')
        except Exception as e:
            self.log(f'Error: {e}')
            self.speak('An error occurred.')
        finally:
            self.listening = False
            self.voice_btn.config(text='🎤 Speak Command')

    def process_command(self, command):
        # Smarter NLP: handle multiple devices, synonyms, and more natural language
        cmd = command.lower()
        # Find all actions (on/off/activate/deactivate)
        actions = []
        if re.search(r'(turn|switch|activate|start|enable|power)\s+(on|up)', cmd):
            actions.append('on')
        if re.search(r'(turn|switch|deactivate|stop|disable|power)\s+(off|down)', cmd):
            actions.append('off')
        if not actions:
            if 'on' in cmd or 'activate' in cmd or 'start' in cmd or 'enable' in cmd:
                actions.append('on')
            if 'off' in cmd or 'deactivate' in cmd or 'stop' in cmd or 'disable' in cmd:
                actions.append('off')
        # Find all mentioned devices
        mentioned = []
        for dev, info in DEVICE_INFO.items():
            for syn in info['synonyms']:
                if re.search(r'\b' + re.escape(syn) + r'\b', cmd):
                    mentioned.append(dev)
                    break
        # If user says 'all', apply to all devices
        if 'all' in cmd or 'everything' in cmd:
            mentioned = list(self.devices.keys())
        # If no action or device found, fallback to old logic
        if not actions:
            if 'on' in cmd:
                actions.append('on')
            elif 'off' in cmd:
                actions.append('off')
        if not mentioned:
            for dev in self.devices:
                if dev.lower() in cmd:
                    mentioned.append(dev)
        # Apply actions
        if mentioned and actions:
            for dev in mentioned:
                self.devices[dev].set_state(actions[0] == 'on')
        else:
            self.log('Command not recognized. Try: "turn on the light" or "switch off the fan".')
            self.speak('Command not recognized. Please try again.')

    def take_screenshot(self):
        # Save screenshot of the app window
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()
        img = ImageGrab.grab((x, y, x + w, y + h))
        img.save('smarthome_screenshot.png')
        self.log('Screenshot saved as smarthome_screenshot.png')
        self.speak('Screenshot saved.')

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def speak(self, text):
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()

    def _speak_thread(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == '__main__':
    app = SmartHomeApp()
    app.mainloop() 