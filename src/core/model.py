import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
from typing import List, Dict, Optional
from src.core.config import settings

class GenrePatternGenerator:
    def __init__(self):
        self.model = None
        self.sequence_length = settings.SEQUENCE_LENGTH
        self.n_features = settings.N_FEATURES
        self.genres = list(settings.GENRE_PATTERNS.keys())
        
    def build_model(self):
        """Build the deep learning model."""
        input_layer = layers.Input(shape=(self.sequence_length, self.n_features))
        
        # LSTM layers for sequence processing
        x = layers.LSTM(256, return_sequences=True)(input_layer)
        x = layers.Dropout(0.3)(x)
        x = layers.LSTM(128)(x)
        x = layers.Dropout(0.3)(x)
        
        # Genre-specific processing
        genre_input = layers.Input(shape=(len(self.genres),))
        genre_embedding = layers.Dense(64)(genre_input)
        
        # Combine sequence and genre information
        combined = layers.Concatenate()([x, genre_embedding])
        
        # Output layers
        x = layers.Dense(256, activation='relu')(combined)
        x = layers.Dropout(0.3)(x)
        output = layers.Dense(self.n_features, activation='sigmoid')(x)
        
        self.model = models.Model(inputs=[input_layer, genre_input], outputs=output)
        
        # Compile model
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50, batch_size: int = 32):
        """Train the model on labeled data."""
        if self.model is None:
            self.build_model()
            
        # Convert genre labels to one-hot encoding
        genre_indices = [self.genres.index(genre) for genre in y]
        genre_one_hot = tf.one_hot(genre_indices, depth=len(self.genres))
        
        # Train the model
        self.model.fit(
            [X, genre_one_hot],
            y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2
        )
        
    def generate_pattern(self, genre: str, length: int = 32) -> np.ndarray:
        """Generate a new pattern for a specific genre."""
        if self.model is None:
            raise ValueError("Model not trained yet")
            
        # Create initial sequence
        initial_sequence = np.zeros((1, self.sequence_length, self.n_features))
        
        # Create genre one-hot encoding
        genre_index = self.genres.index(genre)
        genre_one_hot = tf.one_hot([genre_index], depth=len(self.genres))
        
        # Generate pattern
        pattern = []
        current_sequence = initial_sequence
        
        for _ in range(length):
            # Predict next step
            next_step = self.model.predict([current_sequence, genre_one_hot])
            pattern.append(next_step[0])
            
            # Update sequence
            current_sequence = np.roll(current_sequence, -1, axis=1)
            current_sequence[0, -1] = next_step[0]
            
        return np.array(pattern)
        
    def save_model(self, path: str):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("No model to save")
        self.model.save(path)
        
    def load_model(self, path: str):
        """Load a trained model."""
        self.model = models.load_model(path)
        
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict:
        """Evaluate the model on test data."""
        if self.model is None:
            raise ValueError("Model not trained yet")
            
        # Convert genre labels to one-hot encoding
        genre_indices = [self.genres.index(genre) for genre in y]
        genre_one_hot = tf.one_hot(genre_indices, depth=len(self.genres))
        
        # Evaluate
        metrics = self.model.evaluate([X, genre_one_hot], y, return_dict=True)
        return metrics 