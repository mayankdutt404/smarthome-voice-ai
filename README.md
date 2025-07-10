# Smart Home Voice-Controlled System

A modern, AI-powered smart home simulator that lets you control virtual devices (Light, Fan, AC, Heater) using your voice!  
Built with Python, Tkinter, SpeechRecognition, and pyttsx3.

---

## 🚀 Features

- **Voice Control:** Use natural language to turn devices ON/OFF (e.g., “turn on the light and fan”, “switch off all”).
- **Modern GUI:** Beautiful, responsive interface with device cards and status log.
- **Text-to-Speech Feedback:** The app speaks back the action it takes.
- **Screenshot Button:** Save the current app window for your report/demo.
- **Offline, Fast, and Private:** No cloud required for NLP or TTS.

---

## 🖥️ Demo

![screenshot](smarthome_screenshot.png)

---

## 🛠️ Tech Stack

- Python 3.x
- Tkinter (GUI)
- SpeechRecognition (voice input)
- PyAudio (microphone support)
- pyttsx3 (text-to-speech)
- Pillow (for icons and screenshots)

---

## 📦 Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/mayankdutt404/smarthome-voice-ai.git
   cd smarthome-voice-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ How to Use

1. **Run the app:**
   ```bash
   python smarthome_voice_gui.py
   ```

2. **Control devices:**
   - **Click** on any device card to toggle it ON/OFF.
   - **Click the “🎤 Speak Command” button** and say a command like:
     - “Turn on the light and fan”
     - “Switch off all”
     - “Please activate the heater”
     - “Turn the AC off”
   - The app will recognize your voice, update the devices, and speak back the action.

3. **Take a screenshot:**
   - Click the **📸 Take Screenshot** button to save the current app window as `smarthome_screenshot.png`.

---

## 📚 Extending

- Add more devices or custom icons.
- Integrate with real IoT hardware.
- Swap in advanced AI NLP (e.g., OpenAI) for even more natural language understanding.

---

## 📝 Author

- [mayankdutt404](https://github.com/mayankdutt404)

---

## 📄 License

MIT License
