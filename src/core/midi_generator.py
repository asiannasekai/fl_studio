import pretty_midi
import numpy as np
from typing import List, Dict, Optional
import mido
import rtmidi
from src.core.config import settings
import json
import os

class MIDIGenerator:
    def __init__(self, tempo: int = settings.DEFAULT_TEMPO):
        self.tempo = tempo
        self.pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        self.midi_out = None
        self._initialize_midi_output()
        
    def _initialize_midi_output(self):
        """Initialize MIDI output port."""
        try:
            self.midi_out = rtmidi.MidiOut()
            available_ports = self.midi_out.get_ports()
            
            if settings.MIDI_OUTPUT_PORT and settings.MIDI_OUTPUT_PORT in available_ports:
                port_index = available_ports.index(settings.MIDI_OUTPUT_PORT)
                self.midi_out.open_port(port_index)
            elif available_ports:
                self.midi_out.open_port(0)
        except Exception as e:
            print(f"Warning: Could not initialize MIDI output: {e}")
            self.midi_out = None
            
    def create_pattern(self, pattern_type: str, scenario: str = "loop_based", 
                      variations: int = 1, complexity: int = 1) -> pretty_midi.PrettyMIDI:
        """Generate a complete pattern with multiple instruments and variations."""
        # Clear existing instruments
        self.pm.instruments = []
        
        # Get scenario configuration
        scenario_config = settings.SCENARIOS.get(scenario, settings.SCENARIOS["loop_based"])
        
        # Generate patterns for each section
        for section in scenario_config["sections"]:
            self._generate_section(section, pattern_type, complexity)
            
        # Add variations if requested
        if variations > 1:
            self._add_variations(variations, pattern_type)
            
        # Add transitions if specified in scenario
        if scenario_config.get("transitions", False):
            self._add_transitions()
            
        return self.pm
    
    def _generate_section(self, section: str, pattern_type: str, complexity: int):
        """Generate a specific section of the pattern."""
        # Generate drums
        self.create_drum_pattern(pattern_type, complexity=complexity)
        
        # Generate bass
        self.create_bass_line(pattern_type, complexity=complexity)
        
        # Generate harmony
        self.create_harmony(pattern_type, complexity=complexity)
        
        # Generate melody if complexity is high enough
        if complexity > 1:
            self.create_melody(pattern_type, complexity=complexity)
            
    def create_drum_pattern(self, pattern_type: str, complexity: int = 1) -> pretty_midi.PrettyMIDI:
        """Generate an enhanced drum pattern."""
        drum_program = pretty_midi.Instrument(program=0, is_drum=True)
        
        # Get pattern configuration
        pattern_config = settings.GENRE_PATTERNS.get(pattern_type, {}).get("drums", {})
        
        # Generate basic pattern
        for drum, pattern in pattern_config.items():
            self._add_drum_notes(drum_program, drum, pattern, complexity)
            
        # Add complexity-based variations
        if complexity > 1:
            self._add_drum_fills(drum_program, complexity)
            
        self.pm.instruments.append(drum_program)
        return self.pm
    
    def _add_drum_notes(self, program: pretty_midi.Instrument, drum: str, 
                       pattern: List[int], complexity: int):
        """Add drum notes with velocity variations."""
        drum_notes = {
            'kick': 36,
            'snare': 38,
            'hihat': 42,
            'tom': 45,
            'crash': 49
        }
        
        for i, is_note in enumerate(pattern):
            if is_note:
                velocity = np.random.randint(80, 120)  # Add some variation
                start_time = i * 0.25
                note = pretty_midi.Note(
                    velocity=velocity,
                    pitch=drum_notes.get(drum, 36),
                    start=start_time,
                    end=start_time + 0.2
                )
                program.notes.append(note)
                
    def _add_drum_fills(self, program: pretty_midi.Instrument, complexity: int):
        """Add drum fills based on complexity."""
        if complexity > 2:
            # Add tom fills
            for i in range(4):
                start_time = i * 0.25
                note = pretty_midi.Note(
                    velocity=100,
                    pitch=45,  # Tom
                    start=start_time,
                    end=start_time + 0.2
                )
                program.notes.append(note)
                
    def create_bass_line(self, pattern_type: str, complexity: int = 1) -> pretty_midi.PrettyMIDI:
        """Generate an enhanced bass line."""
        bass_program = pretty_midi.Instrument(program=32)  # Acoustic Bass
        
        # Get pattern configuration
        pattern_config = settings.GENRE_PATTERNS.get(pattern_type, {}).get("bass", {})
        
        # Generate notes
        for i, rhythm in enumerate(pattern_config.get("rhythm", [])):
            if rhythm:
                note = pattern_config.get("notes", ["C2"])[i % len(pattern_config.get("notes", ["C2"]))]
                start_time = i * 0.25
                note_obj = pretty_midi.Note(
                    velocity=100,
                    pitch=self._note_to_midi(note),
                    start=start_time,
                    end=start_time + 0.5
                )
                bass_program.notes.append(note_obj)
                
        self.pm.instruments.append(bass_program)
        return self.pm
    
    def create_harmony(self, pattern_type: str, complexity: int = 1) -> pretty_midi.PrettyMIDI:
        """Generate harmony parts."""
        harmony_program = pretty_midi.Instrument(program=0)  # Piano
        
        # Basic chord progression based on genre
        chords = self._get_chord_progression(pattern_type)
        
        for i, chord in enumerate(chords):
            start_time = i * 1.0  # One chord per bar
            for note in chord:
                note_obj = pretty_midi.Note(
                    velocity=80,
                    pitch=self._note_to_midi(note),
                    start=start_time,
                    end=start_time + 1.0
                )
                harmony_program.notes.append(note_obj)
                
        self.pm.instruments.append(harmony_program)
        return self.pm
    
    def create_melody(self, pattern_type: str, complexity: int = 1) -> pretty_midi.PrettyMIDI:
        """Generate a melody line."""
        melody_program = pretty_midi.Instrument(program=73)  # Flute
        
        # Generate simple melody based on chord progression
        chords = self._get_chord_progression(pattern_type)
        
        for i, chord in enumerate(chords):
            start_time = i * 1.0
            # Select a note from the chord
            note = chord[np.random.randint(0, len(chord))]
            note_obj = pretty_midi.Note(
                velocity=90,
                pitch=self._note_to_midi(note) + 12,  # One octave higher
                start=start_time,
                end=start_time + 0.5
            )
            melody_program.notes.append(note_obj)
            
        self.pm.instruments.append(melody_program)
        return self.pm
    
    def _note_to_midi(self, note: str) -> int:
        """Convert note name to MIDI pitch number."""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_name = note[:-1]
        octave = int(note[-1])
        return notes.index(note_name) + (octave + 1) * 12
        
    def _get_chord_progression(self, pattern_type: str) -> List[List[str]]:
        """Get chord progression based on genre."""
        progressions = {
            'reggae': [
                ['C2', 'E2', 'G2'],
                ['G2', 'B2', 'D3'],
                ['A2', 'C3', 'E3'],
                ['F2', 'A2', 'C3']
            ],
            'hiphop': [
                ['C2', 'F2', 'A2'],
                ['F2', 'A2', 'C3'],
                ['G2', 'B2', 'D3'],
                ['A2', 'C3', 'E3']
            ],
            'edm': [
                ['C2', 'E2', 'G2'],
                ['G2', 'B2', 'D3'],
                ['A2', 'C3', 'E3'],
                ['F2', 'A2', 'C3']
            ]
        }
        return progressions.get(pattern_type, progressions['reggae'])
        
    def _add_variations(self, count: int, pattern_type: str):
        """Add variations to the pattern."""
        for i in range(1, count):
            variation = self.create_pattern(pattern_type, complexity=i+1)
            # Merge variations with original pattern
            for instrument in variation.instruments:
                self.pm.instruments.append(instrument)
                
    def _add_transitions(self):
        """Add transitions between sections."""
        # Implement transition logic here
        pass
        
    def save_midi(self, filename: str):
        """Save the generated MIDI to a file."""
        self.pm.write(filename)
        
    def play_realtime(self):
        """Play the pattern in real-time through MIDI output."""
        if not self.midi_out:
            raise RuntimeError("MIDI output not initialized")
            
        # Convert PrettyMIDI to MIDI messages and send them
        for instrument in self.pm.instruments:
            for note in instrument.notes:
                # Note on
                self.midi_out.send_message([0x90, note.pitch, note.velocity])
                # Note off
                self.midi_out.send_message([0x80, note.pitch, 0])
                
    def export_to_fl_studio(self, filename: str):
        """Export MIDI file in a format compatible with FL Studio."""
        self.save_midi(filename)
        
    def __del__(self):
        """Clean up MIDI resources."""
        if self.midi_out:
            self.midi_out.close_port() 