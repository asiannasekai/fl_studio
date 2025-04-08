import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from src.core.config import settings
from src.core.midi_generator import MIDIGenerator

class Project:
    def __init__(self, name: str, user: str = settings.DEFAULT_USER):
        self.name = name
        self.user = user
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.scenario = "loop_based"
        self.genre = "reggae"
        self.tempo = settings.DEFAULT_TEMPO
        self.complexity = 1
        self.variations = 1
        self.sections: List[Dict] = []
        self.midi_generator = MIDIGenerator(tempo=self.tempo)
        
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "user": self.user,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "scenario": self.scenario,
            "genre": self.genre,
            "tempo": self.tempo,
            "complexity": self.complexity,
            "variations": self.variations,
            "sections": self.sections
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        project = cls(data["name"], data["user"])
        project.created_at = data["created_at"]
        project.updated_at = data["updated_at"]
        project.scenario = data["scenario"]
        project.genre = data["genre"]
        project.tempo = data["tempo"]
        project.complexity = data["complexity"]
        project.variations = data["variations"]
        project.sections = data["sections"]
        return project
        
    def generate_pattern(self) -> str:
        """Generate MIDI pattern and save it."""
        self.midi_generator.tempo = self.tempo
        self.midi_generator.create_pattern(
            self.genre,
            self.scenario,
            self.variations,
            self.complexity
        )
        
        # Save the MIDI file
        filename = f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
        output_path = os.path.join(settings.EXPORTS_DIR, self.user, filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        self.midi_generator.save_midi(output_path)
        return output_path
        
    def play_realtime(self):
        """Play the pattern in real-time."""
        self.midi_generator.tempo = self.tempo
        self.midi_generator.create_pattern(
            self.genre,
            self.scenario,
            self.variations,
            self.complexity
        )
        self.midi_generator.play_realtime()

class ProjectManager:
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self._load_projects()
        
    def _load_projects(self):
        """Load projects from disk."""
        projects_dir = settings.PROJECTS_DIR
        if not os.path.exists(projects_dir):
            return
            
        for user_dir in os.listdir(projects_dir):
            user_path = os.path.join(projects_dir, user_dir)
            if os.path.isdir(user_path):
                for project_file in os.listdir(user_path):
                    if project_file.endswith('.json'):
                        with open(os.path.join(user_path, project_file), 'r') as f:
                            data = json.load(f)
                            project = Project.from_dict(data)
                            self.projects[f"{user_dir}/{project.name}"] = project
                            
    def _save_project(self, project: Project):
        """Save project to disk."""
        project_dir = os.path.join(settings.PROJECTS_DIR, project.user)
        os.makedirs(project_dir, exist_ok=True)
        
        project_file = os.path.join(project_dir, f"{project.name}.json")
        with open(project_file, 'w') as f:
            json.dump(project.to_dict(), f, indent=2)
            
    def create_project(self, name: str, user: str = settings.DEFAULT_USER) -> Project:
        """Create a new project."""
        if f"{user}/{name}" in self.projects:
            raise ValueError(f"Project {name} already exists for user {user}")
            
        project = Project(name, user)
        self.projects[f"{user}/{name}"] = project
        self._save_project(project)
        return project
        
    def get_project(self, name: str, user: str = settings.DEFAULT_USER) -> Optional[Project]:
        """Get a project by name and user."""
        return self.projects.get(f"{user}/{name}")
        
    def update_project(self, project: Project):
        """Update a project."""
        project.updated_at = datetime.now().isoformat()
        self.projects[f"{project.user}/{project.name}"] = project
        self._save_project(project)
        
    def delete_project(self, name: str, user: str = settings.DEFAULT_USER):
        """Delete a project."""
        project_key = f"{user}/{name}"
        if project_key in self.projects:
            del self.projects[project_key]
            project_file = os.path.join(settings.PROJECTS_DIR, user, f"{name}.json")
            if os.path.exists(project_file):
                os.remove(project_file)
                
    def list_projects(self, user: str = settings.DEFAULT_USER) -> List[Project]:
        """List all projects for a user."""
        return [p for k, p in self.projects.items() if k.startswith(f"{user}/")]
        
    def generate_all_patterns(self, user: str = settings.DEFAULT_USER) -> List[str]:
        """Generate patterns for all projects of a user."""
        generated_files = []
        for project in self.list_projects(user):
            try:
                output_path = project.generate_pattern()
                generated_files.append(output_path)
            except Exception as e:
                print(f"Error generating pattern for project {project.name}: {e}")
        return generated_files 