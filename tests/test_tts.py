import pyttsx3
import time

def test_tts_initialization():
    """Test if TTS engine can be initialized."""
    print("Testing TTS initialization...")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        
        print(f"TTS initialized successfully")
        print(f"Available voices: {len(voices)}")
        print(f"Current rate: {rate}")
        print(f"Current volume: {volume}")
        
        engine.stop()
        return True
    except Exception as e:
        print(f"TTS initialization failed: {e}")
        return False

def test_tts_speak():
    """Test TTS speech functionality."""
    print("\nTesting TTS speech...")
    try:
        engine = pyttsx3.init()
        
        # Set properties
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Test speech
        test_text = "This is a test of the text to speech system"
        print(f"Speaking: '{test_text}'")
        
        engine.say(test_text)
        engine.runAndWait()
        
        engine.stop()
        return True
    except Exception as e:
        print(f"TTS speech test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== TTS Component Tests ===")
    
    init_ok = test_tts_initialization()
    print(f"TTS initialization test: {'PASSED' if init_ok else 'FAILED'}")
    
    if init_ok:
        speak_ok = test_tts_speak()
        print(f"TTS speech test: {'PASSED' if speak_ok else 'FAILED'}") 