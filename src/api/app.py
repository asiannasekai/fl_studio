from flask import Flask, request, jsonify, send_file
from src.core.project_manager import ProjectManager
from src.core.config import settings
import os
from typing import Dict, List
import json

app = Flask(__name__)
project_manager = ProjectManager()

@app.route('/api/projects', methods=['GET'])
def list_projects():
    user = request.args.get('user', settings.DEFAULT_USER)
    projects = project_manager.list_projects(user)
    return jsonify([p.to_dict() for p in projects])

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    name = data.get('name')
    user = data.get('user', settings.DEFAULT_USER)
    
    if not name:
        return jsonify({'error': 'Project name is required'}), 400
        
    try:
        project = project_manager.create_project(name, user)
        return jsonify(project.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/projects/<name>', methods=['GET'])
def get_project(name):
    user = request.args.get('user', settings.DEFAULT_USER)
    project = project_manager.get_project(name, user)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    return jsonify(project.to_dict())

@app.route('/api/projects/<name>', methods=['PUT'])
def update_project(name):
    user = request.args.get('user', settings.DEFAULT_USER)
    project = project_manager.get_project(name, user)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    data = request.json
    for key, value in data.items():
        if hasattr(project, key):
            setattr(project, key, value)
            
    project_manager.update_project(project)
    return jsonify(project.to_dict())

@app.route('/api/projects/<name>', methods=['DELETE'])
def delete_project(name):
    user = request.args.get('user', settings.DEFAULT_USER)
    project = project_manager.get_project(name, user)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    project_manager.delete_project(name, user)
    return jsonify({'message': 'Project deleted'})

@app.route('/api/projects/<name>/generate', methods=['POST'])
def generate_pattern(name):
    user = request.args.get('user', settings.DEFAULT_USER)
    project = project_manager.get_project(name, user)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    try:
        output_path = project.generate_pattern()
        return jsonify({
            'status': 'success',
            'message': 'Pattern generated successfully',
            'file_path': output_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<name>/play', methods=['POST'])
def play_pattern(name):
    user = request.args.get('user', settings.DEFAULT_USER)
    project = project_manager.get_project(name, user)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    try:
        project.play_realtime()
        return jsonify({'status': 'success', 'message': 'Playing pattern'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scenarios', methods=['GET'])
def list_scenarios():
    return jsonify(settings.SCENARIOS)

@app.route('/api/genres', methods=['GET'])
def list_genres():
    return jsonify(list(settings.GENRE_PATTERNS.keys()))

@app.route('/api/export/<name>', methods=['GET'])
def export_project(name):
    user = request.args.get('user', settings.DEFAULT_USER)
    project = project_manager.get_project(name, user)
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    try:
        output_path = project.generate_pattern()
        return send_file(
            output_path,
            mimetype='audio/midi',
            as_attachment=True,
            download_name=f"{name}.mid"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=settings.DEBUG, port=5000) 