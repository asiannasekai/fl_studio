from src.core.config import Settings

def test_settings_initialization():
    """Test that settings can be initialized correctly."""
    settings = Settings()
    assert settings.SEQUENCE_LENGTH == 32
    assert settings.N_FEATURES == 4
    assert settings.BATCH_SIZE == 32
    assert settings.EPOCHS == 100
    assert settings.LEARNING_RATE == 0.001
    assert settings.DROPOUT_RATE == 0.2
    assert settings.HIDDEN_UNITS == 256
    assert settings.NUM_LAYERS == 2

def test_genre_patterns():
    """Test that genre patterns are correctly defined."""
    settings = Settings()
    assert 'house' in settings.GENRE_PATTERNS
    assert 'techno' in settings.GENRE_PATTERNS
    assert 'dubstep' in settings.GENRE_PATTERNS
    
    # Test house pattern structure
    house_patterns = settings.GENRE_PATTERNS['house']
    assert 'kick' in house_patterns
    assert 'snare' in house_patterns
    assert 'hihat' in house_patterns 