import pyttsx3

class TTSSpeaker:
    """Handles text-to-speech conversion."""

    def __init__(self):
        print("Initializing TTS engine...")
        self.engine = pyttsx3.init()
        self.setup_voice()
        print("TTS engine initialized successfully")

    def setup_voice(self):
        """Configure the TTS voice settings."""
        print("Setting up TTS voice...")
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        print("TTS voice setup complete")

    def speak(self, text):
        """Convert text to speech."""
        if text and text.strip():
            print(f"TTS speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            print("TTS finished speaking")

    def __del__(self):
        """Clean up TTS resources."""
        print("Cleaning up TTS resources...")
        self.engine.stop()
        try:
            self.engine.endLoop()
        except:
            pass
        print("TTS cleanup complete") 