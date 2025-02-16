import time
from typing import List, Tuple
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
    # Calculate envelope timings (10ms attack and release)
    attack_time = min(0.01, duration * 0.1)  # 10ms or 10% of duration, whichever is shorter
    release_time = attack_time
    sustain_time = duration - (attack_time + release_time)

    # Create the envelope with proper timing
    attack = np.linspace(0, 1, int(sample_rate * attack_time))
    sustain = np.ones(int(sample_rate * sustain_time))
    release = np.linspace(1, 0, int(sample_rate * release_time))

    # Combine envelope parts
    envelope = np.concatenate([attack, sustain, release])

    # Ensure envelope matches wave length exactly
    if len(envelope) > len(wave):
        envelope = envelope[:len(wave)]
    elif len(envelope) < len(wave):
        envelope = np.pad(envelope, (0, len(wave) - len(envelope)), 'edge')

    return wave * envelope

def play_wave(wave, sample_rate=44100):
    """
    Play the generated wave through the default audio output.

    Parameters:
    wave (numpy.ndarray): The waveform to play
    sample_rate (int): Number of samples per second
    """
    sd.play(wave, sample_rate)
    sd.wait()  # Wait until the sound has finished playing

def generate_note(note, duration=1.0, sample_rate=44100, amplitude=0.5):
    """
    Generate a note with the given pitch and duration.

    Parameters:
    note (str): The note to generate (e.g., "A4")
    duration (float): Duration of the sound in seconds
    sample_rate (int): Number of samples per second
    amplitude (float): Amplitude of the wave (between 0 and 1)

    Returns:
    numpy.ndarray: The generated waveform
    """
    frequency = NOTES.get(note)
    if frequency is None:
        raise ValueError(f"Unknown note: {note}")
    return generate_wave(frequency, duration, sample_rate, amplitude)

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
PIANO_KEYS = [
    "C4",
    "C#4",
    "D4",
    "D#4",
    "E4",
    "F4",
    "F#4",
    "G4",
    "G#4",
    "A4",
    "A#4",
    "B4",
    "C5",
    'C#5',
    'D5',
    'D#5']

NOTES = {
    "C3": 130.81,
    "C#3": 138.59,
    "D3": 146.83,
    "D#3": 155.56,
    "E3": 164.81,
    "F3": 174.61,
    "F#3": 185.00,
    "G3": 196.00,
    "G#3": 207.65,
    "A3": 220.00,
    "A#3": 233.08,
    "B3": 246.94,
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
    "C#5": 554.37,
    "D5": 587.33,
    "D#5": 622.25,
}

def parse_note_file(filename: str) -> List[Tuple[float, str, float]]:
    """
    Read and parse a file containing timestamped notes.

    Parameters:
    filename: Path to the file containing notes

    Returns:
    List of tuples containing (timestamp, note)
    """
    # First, read all timestamps and notes
    raw_notes = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('-')
            if len(parts) == 2:
                timestamp = float(parts[0].strip())
                note = parts[1].strip()
                raw_notes.append((timestamp, note))

    # Sort notes by timestamp
    raw_notes.sort(key=lambda x: x[0])

    # Calculate durations based on the time until the next note
    notes_with_duration = []
    for i in range(len(raw_notes)):
        timestamp, note = raw_notes[i]

        # Calculate duration until next note
        if i < len(raw_notes) - 1:
            next_timestamp = raw_notes[i + 1][0]
            duration = next_timestamp - timestamp
        else:
            # For the last note, use a default duration of 0.3 seconds
            duration = 0.3

        notes_with_duration.append((timestamp, note, duration))

    return notes_with_duration

def play_sequence(filename: str):
    """
    Play the sequence with precise timing and durations.
    """
    # Parse notes with their calculated durations
    parsed_notes = parse_note_file(filename)
    start_time = time.time()

    print("Starting playback...")
    print("Timestamp | Note | Duration")
    print("-" * 30)

    for timestamp, note, duration in parsed_notes:
        # Calculate wait time
        current_time = time.time() - start_time
        wait_time = timestamp - current_time

        # Wait if necessary
        if wait_time > 0:
            time.sleep(wait_time)

        # Play the note with its calculated duration
        if note in NOTES.keys():
            wave = generate_note(note, duration)
            play_wave(wave)
            print(f"{timestamp:.2f}s    | {note:3} | {duration:.3f}s")
        else:
            print(f"Unknown note: {note}")

def generate_piano_notes():
    # Generate a sequence of notes
    for note in PIANO_KEYS:
        print("Generando las notas del piano")
        wave = generate_wave(NOTES[note], duration=0.2)
        print(f"Saving {note}.wav ({NOTES[note]} Hz)")
        save_wave(wave, f"notes/{note}.wav")

if __name__ == "__main__":
    play_sequence("notes.txt")
