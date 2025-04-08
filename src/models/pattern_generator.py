import tensorflow as tf
import numpy as np
from typing import List, Dict

class PatternGenerator:
    def __init__(self, sequence_length: int = 32, n_features: int = 128):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = self._build_model()
        
    def _build_model(self) -> tf.keras.Model:
        """Build the LSTM model for pattern generation."""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(256, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(128, return_sequences=True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(self.n_features, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def generate_pattern(self, genre: str, length: int = 32) -> np.ndarray:
        """Generate a new pattern based on genre."""
        # For now, we'll use predefined patterns until we train the model
        patterns = {
            'reggae': self._generate_reggae_pattern(length),
            'hiphop': self._generate_hiphop_pattern(length)
        }
        
        if genre not in patterns:
            raise ValueError(f"Unsupported genre: {genre}")
            
        return patterns[genre]
    
    def _generate_reggae_pattern(self, length: int) -> np.ndarray:
        """Generate a reggae-style pattern."""
        pattern = np.zeros((length, self.n_features))
        
        # Add kick drum on beats 1 and 3
        for i in range(0, length, 8):
            pattern[i, 36] = 1  # Kick drum
            pattern[i + 4, 36] = 1
            
        # Add snare on beats 2 and 4
        for i in range(2, length, 8):
            pattern[i, 38] = 1  # Snare
            pattern[i + 4, 38] = 1
            
        # Add hi-hat on eighth notes
        for i in range(length):
            if i % 2 == 0:
                pattern[i, 42] = 1  # Hi-hat
                
        return pattern
    
    def _generate_hiphop_pattern(self, length: int) -> np.ndarray:
        """Generate a hip-hop style pattern."""
        pattern = np.zeros((length, self.n_features))
        
        # Add kick drum
        for i in [0, 4, 8, 12, 16, 20, 24, 28]:
            pattern[i, 36] = 1  # Kick drum
            
        # Add snare on beats 2 and 4
        for i in range(2, length, 8):
            pattern[i, 38] = 1  # Snare
            pattern[i + 4, 38] = 1
            
        # Add hi-hat
        for i in range(length):
            if i % 2 == 0:
                pattern[i, 42] = 1  # Hi-hat
                
        return pattern 