import os
import json
import shutil
from typing import Dict, Any, Optional, List

class Storage:
    """Handles persistent storage for LLMPromptKit."""
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def ensure_dir(self, dir_path: str) -> str:
        """Ensure directory exists and return its path."""
        full_path = os.path.join(self.base_path, dir_path)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def save_json(self, dir_path: str, filename: str, data: Dict[str, Any]) -> str:
        """Save data to a JSON file."""
        dir_full_path = self.ensure_dir(dir_path)
        file_path = os.path.join(dir_full_path, f"{filename}.json")
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return file_path

    def load_json(self, dir_path: str, filename: str) -> Optional[Dict[str, Any]]:
        """Load data from a JSON file."""
        file_path = os.path.join(self.base_path, dir_path, f"{filename}.json")
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, "r") as f:
            return json.load(f)

    def list_files(self, dir_path: str, extension: Optional[str] = None) -> List[str]:
        """List files in a directory, optionally filtered by extension."""
        full_path = os.path.join(self.base_path, dir_path)
        
        if not os.path.exists(full_path):
            return []
        
        files = os.listdir(full_path)
        
        if extension:
            return [f for f in files if f.endswith(extension)]
        
        return files

    def delete_file(self, dir_path: str, filename: str) -> bool:
        """Delete a file."""
        file_path = os.path.join(self.base_path, dir_path, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        
        return False

    def backup(self, backup_path: Optional[str] = None) -> str:
        """Create a backup of the entire storage."""
        if not backup_path:
            backup_path = f"{self.base_path}_backup"
        
        shutil.make_archive(backup_path, "zip", self.base_path)
        return f"{backup_path}.zip"

    def restore(self, backup_path: str) -> bool:
        """Restore from a backup archive."""
        if not os.path.exists(backup_path):
            return False
        
        shutil.rmtree(self.base_path, ignore_errors=True)
        os.makedirs(self.base_path, exist_ok=True)
        
        shutil.unpack_archive(backup_path, self.base_path)
        return True