from pydantic_settings import BaseSettings
from typing import Dict, List, Optional, Tuple
import os
from dataclasses import dataclass

@dataclass
class Settings:
    # Model settings
    SEQUENCE_LENGTH: int = 32
    N_FEATURES: int = 4  # pitch, velocity, duration, time_since_last
    BATCH_SIZE: int = 32
    EPOCHS: int = 100
    LEARNING_RATE: float = 0.001
    DROPOUT_RATE: float = 0.2
    HIDDEN_UNITS: int = 256
    NUM_LAYERS: int = 2

    # Genre patterns
    GENRE_PATTERNS: Dict[str, Dict[str, List[Tuple[int, int]]]] = {
        'house': {
            'kick': [(0, 1), (4, 1), (8, 1), (12, 1)],  # 4/4 kick pattern
            'snare': [(4, 1), (12, 1)],  # Backbeat snare
            'hihat': [(0, 0.5), (2, 0.5), (4, 0.5), (6, 0.5), (8, 0.5), (10, 0.5), (12, 0.5), (14, 0.5)]  # 8th notes
        },
        'techno': {
            'kick': [(0, 1), (4, 1), (8, 1), (12, 1)],  # 4/4 kick pattern
            'snare': [(4, 1), (12, 1)],  # Backbeat snare
            'hihat': [(0, 0.25), (1, 0.25), (2, 0.25), (3, 0.25), (4, 0.25), (5, 0.25), (6, 0.25), (7, 0.25),
                     (8, 0.25), (9, 0.25), (10, 0.25), (11, 0.25), (12, 0.25), (13, 0.25), (14, 0.25), (15, 0.25)]  # 16th notes
        },
        'dubstep': {
            'kick': [(0, 1), (8, 1)],  # Half-time kick pattern
            'snare': [(4, 1), (12, 1)],  # Backbeat snare
            'hihat': [(0, 0.5), (2, 0.5), (4, 0.5), (6, 0.5), (8, 0.5), (10, 0.5), (12, 0.5), (14, 0.5)]  # 8th notes
        }
    }

    # BPM ranges for each genre
    BPM_RANGES: Dict[str, Tuple[int, int]] = {
        'house': (120, 130),
        'techno': (125, 140),
        'dubstep': (140, 150)
    }

    # Data processing settings
    DATA_DIR: str = 'data/raw'
    PROCESSED_DATA_DIR: str = 'data/processed'
    MODEL_DIR: str = 'models'
    TRAIN_TEST_SPLIT: float = 0.8

    # Feature extraction settings
    NOTE_FEATURES: List[str] = ['pitch', 'velocity', 'duration', 'time_since_last']
    MAX_VELOCITY: int = 127
    MAX_DURATION: float = 4.0  # Maximum note duration in beats
    MAX_TIME_SINCE_LAST: float = 4.0  # Maximum time between notes in beats

    # Training settings
    EARLY_STOPPING_PATIENCE: int = 10
    VALIDATION_SPLIT: float = 0.2
    MIN_DELTA: float = 0.001

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "FL Studio AI Assistant Pro"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # MIDI settings
    MIDI_OUTPUT_PORT: Optional[str] = None
    DEFAULT_TEMPO: int = 120
    DEFAULT_TIME_SIGNATURE: str = "4/4"
    
    # AI Model settings
    MODEL_PATH: str = "models/weights"
    
    # Storage settings
    PROJECTS_DIR: str = "projects"
    TEMPLATES_DIR: str = "templates"
    EXPORTS_DIR: str = "exports"
    
    # User settings
    DEFAULT_USER: str = "default"
    MAX_PROJECTS_PER_USER: int = 100
    
    # Scenario templates
    SCENARIOS: Dict[str, Dict] = {
        "full_song": {
            "sections": ["intro", "verse", "chorus", "bridge", "outro"],
            "transitions": True,
            "variations": True
        },
        "loop_based": {
            "sections": ["main_loop", "variation_1", "variation_2"],
            "transitions": False,
            "variations": True
        },
        "live_performance": {
            "sections": ["intro", "main", "breakdown", "build", "drop"],
            "transitions": True,
            "variations": True
        }
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Create necessary directories
for directory in [settings.PROJECTS_DIR, settings.TEMPLATES_DIR, settings.EXPORTS_DIR, settings.MODEL_PATH]:
    os.makedirs(directory, exist_ok=True) 