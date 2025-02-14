import numpy as np
from scipy.io import wavfile
import sounddevice as sd

def generate_wave(frequency, duration=1.0, sample_rate=44100, amplitude=0.5):
    """
    Generate a sine wave with the given frequency and duration.
    
    Parameters:
    frequency (float): Frequency of the wave in Hz
    duration (float): Duration of the sound in seconds
    sample_rate (int): Number of samples per second
    amplitude (float): Amplitude of the wave (between 0 and 1)
    
    Returns:
    numpy.ndarray: The generated waveform
    """
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def play_wave(wave, sample_rate=44100):
    """
    Play the generated wave through the default audio output.
    
    Parameters:
    wave (numpy.ndarray): The waveform to play
    sample_rate (int): Number of samples per second
    """
    sd.play(wave, sample_rate)
    sd.wait()  # Wait until the sound has finished playing

def save_wave(wave, filename, sample_rate=44100):
    """
    Save the wave to a WAV file.
    
    Parameters:
    wave (numpy.ndarray): The waveform to save
    filename (str): Output filename (should end with .wav)
    sample_rate (int): Number of samples per second
    """
    # Convert to 16-bit integers
    wave_int = np.int16(wave * 32767)
    wavfile.write(filename, sample_rate, wave_int)

# Dictionary of musical notes and their frequencies (A4 = 440Hz)
NOTES = {
    "C4": 261.63,
    "C#4": 277.18,
    "D4": 293.66,
    "D#4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "A4": 440.00,
    "A#4": 466.16,
    "B4": 493.88,
    "C5": 523.25,
    'C#5': 554.37,
    'D5': 587.33,
    'D#5': 622.25,
}

# Example usage
if __name__ == "__main__":
    # Generate a sequence of notes
    for note in NOTES:
        wave = generate_wave(NOTES[note], duration=0.2)
        print(f"Playing and saving {note}.wav ({NOTES[note]} Hz)")
        play_wave(wave)
        save_wave(wave, f"{note}.wav")