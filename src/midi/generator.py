import pretty_midi
import numpy as np
from typing import List, Dict, Optional
import mido

class MIDIGenerator:
    def __init__(self, tempo: int = 120):
        self.tempo = tempo
        self.pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        
    def create_drum_pattern(self, pattern_type: str = 'reggae', bars: int = 4) -> pretty_midi.PrettyMIDI:
        """Generate a drum pattern based on genre and number of bars."""
        drum_program = pretty_midi.Instrument(program=0, is_drum=True)
        
        # Define common drum patterns
        patterns = {
            'reggae': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 0],  # On beats 1 and 3
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],  # On beats 2 and 4
                'hihat': [1, 1, 1, 1, 1, 1, 1, 1],  # Eighth notes
            },
            'hiphop': {
                'kick': [1, 0, 0, 0, 1, 0, 0, 1],
                'snare': [0, 0, 1, 0, 0, 0, 1, 0],
                'hihat': [1, 0, 1, 0, 1, 0, 1, 0],
            }
        }
        
        if pattern_type not in patterns:
            raise ValueError(f"Unsupported pattern type: {pattern_type}")
            
        pattern = patterns[pattern_type]
        
        # MIDI note numbers for drums
        drum_notes = {
            'kick': 36,  # C1
            'snare': 38,  # D1
            'hihat': 42,  # F#1
        }
        
        # Generate notes for each drum
        for drum, notes in pattern.items():
            for bar in range(bars):
                for step, is_note in enumerate(notes):
                    if is_note:
                        start_time = (bar * 8 + step) * 0.25  # 0.25 = eighth note
                        note = pretty_midi.Note(
                            velocity=100,
                            pitch=drum_notes[drum],
                            start=start_time,
                            end=start_time + 0.2
                        )
                        drum_program.notes.append(note)
        
        self.pm.instruments.append(drum_program)
        return self.pm
    
    def create_bass_line(self, key: str = 'C', pattern_type: str = 'reggae', bars: int = 4) -> pretty_midi.PrettyMIDI:
        """Generate a bass line based on key and genre."""
        bass_program = pretty_midi.Instrument(program=32)  # Acoustic Bass
        
        # Define bass patterns
        patterns = {
            'reggae': {
                'notes': [0, 0, 0, 0, 0, 0, 0, 0],  # Will be filled with actual notes
                'rhythm': [1, 0, 0, 0, 1, 0, 0, 0],  # On beats 1 and 3
            }
        }
        
        if pattern_type not in patterns:
            raise ValueError(f"Unsupported pattern type: {pattern_type}")
            
        pattern = patterns[pattern_type]
        
        # Generate notes
        for bar in range(bars):
            for step, is_note in enumerate(pattern['rhythm']):
                if is_note:
                    start_time = (bar * 8 + step) * 0.25
                    note = pretty_midi.Note(
                        velocity=100,
                        pitch=48,  # C2
                        start=start_time,
                        end=start_time + 0.5
                    )
                    bass_program.notes.append(note)
        
        self.pm.instruments.append(bass_program)
        return self.pm
    
    def save_midi(self, filename: str):
        """Save the generated MIDI to a file."""
        self.pm.write(filename)
        
    def export_to_fl_studio(self, filename: str):
        """Export MIDI file in a format compatible with FL Studio."""
        self.save_midi(filename) 