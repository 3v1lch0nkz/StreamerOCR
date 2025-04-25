import pyttsx3

class TTSSpeaker:
    """Handles text-to-speech conversion."""

    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()

    def setup_voice(self):
        """Configure the TTS voice settings."""
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    def speak(self, text):
        """Convert text to speech."""
        if text and text.strip():
            self.engine.say(text)
            self.engine.runAndWait()

    def __del__(self):
        """Clean up TTS resources."""
        self.engine.stop()
        try:
            self.engine.endLoop()
        except:
            pass 