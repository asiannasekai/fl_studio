from api.app import app
import os

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('output', exist_ok=True)
    os.makedirs('src/static', exist_ok=True)
    
    # Run the Flask application
    app.run(debug=True, port=5000) 