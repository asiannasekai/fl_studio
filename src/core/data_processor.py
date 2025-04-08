import pretty_midi
import numpy as np
from typing import List, Dict, Tuple
import os
from pathlib import Path
import json
from src.core.config import settings

class DataProcessor:
    def __init__(self):
        self.sequence_length = settings.SEQUENCE_LENGTH
        self.n_features = settings.N_FEATURES
        
    def load_midi_file(self, file_path: str) -> pretty_midi.PrettyMIDI:
        """Load a MIDI file and return a PrettyMIDI object."""
        try:
            return pretty_midi.PrettyMIDI(file_path)
        except Exception as e:
            print(f"Error loading MIDI file {file_path}: {e}")
            return None
            
    def extract_features(self, midi: pretty_midi.PrettyMIDI) -> np.ndarray:
        """Extract features from a MIDI file."""
        # Initialize feature matrix
        features = np.zeros((self.sequence_length, self.n_features))
        
        # Extract note features
        for instrument in midi.instruments:
            for note in instrument.notes:
                # Convert time to sequence index
                start_idx = int(note.start * midi.get_tempo_changes()[1][0] / 60)
                if start_idx >= self.sequence_length:
                    continue
                    
                # Add note features
                features[start_idx, note.pitch] = note.velocity / 127.0
                
        return features
        
    def process_dataset(self, dataset_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Process a dataset of MIDI files with genre labels."""
        X = []
        y = []
        
        # Load dataset metadata
        metadata_path = os.path.join(dataset_path, 'metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
        # Process each file
        for file_info in metadata:
            file_path = os.path.join(dataset_path, file_info['file'])
            genre = file_info['genre']
            
            midi = self.load_midi_file(file_path)
            if midi is None:
                continue
                
            features = self.extract_features(midi)
            X.append(features)
            y.append(genre)
            
        return np.array(X), np.array(y)
        
    def create_sequence_dataset(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for training."""
        sequences = []
        labels = []
        
        for i in range(len(X) - self.sequence_length):
            sequences.append(X[i:i + self.sequence_length])
            labels.append(y[i + self.sequence_length])
            
        return np.array(sequences), np.array(labels)
        
    def save_processed_data(self, X: np.ndarray, y: np.ndarray, output_path: str):
        """Save processed data to disk."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        np.savez(output_path, X=X, y=y)
        
    def load_processed_data(self, input_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Load processed data from disk."""
        data = np.load(input_path)
        return data['X'], data['y'] 