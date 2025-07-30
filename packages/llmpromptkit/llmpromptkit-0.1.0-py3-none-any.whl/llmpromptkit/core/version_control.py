import os
import json
import datetime
from typing import Dict, List, Optional, Any
from .prompt_manager import Prompt, PromptManager

class PromptVersion:
    """Represents a specific version of a prompt."""
    def __init__(
        self, 
        prompt_id: str,
        version: int,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        commit_message: Optional[str] = None
    ):
        self.prompt_id = prompt_id
        self.version = version
        self.content = content
        self.metadata = metadata or {}
        self.commit_message = commit_message or ""
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert version to dictionary."""
        return {
            "prompt_id": self.prompt_id,
            "version": self.version,
            "content": self.content,
            "metadata": self.metadata,
            "commit_message": self.commit_message,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptVersion":
        """Create version from dictionary."""
        return cls(
            prompt_id=data["prompt_id"],
            version=data["version"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            commit_message=data.get("commit_message", "")
        )


class VersionControl:
    """Manages versioning for prompts."""
    def __init__(self, prompt_manager: PromptManager):
        self.prompt_manager = prompt_manager
        self.storage_path = os.path.join(prompt_manager.storage_path, "versions")
        os.makedirs(self.storage_path, exist_ok=True)
        self.versions: Dict[str, Dict[int, PromptVersion]] = {}
        self._load_versions()

    def _load_versions(self) -> None:
        """Load versions from storage."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            return

        for prompt_id_dir in os.listdir(self.storage_path):
            prompt_dir = os.path.join(self.storage_path, prompt_id_dir)
            if os.path.isdir(prompt_dir):
                self.versions[prompt_id_dir] = {}
                
                for filename in os.listdir(prompt_dir):
                    if filename.endswith(".json"):
                        with open(os.path.join(prompt_dir, filename), "r") as f:
                            version_data = json.load(f)
                            version = PromptVersion.from_dict(version_data)
                            self.versions[prompt_id_dir][version.version] = version

    def _save_version(self, version: PromptVersion) -> None:
        """Save version to storage."""
        prompt_dir = os.path.join(self.storage_path, version.prompt_id)
        os.makedirs(prompt_dir, exist_ok=True)
        
        version_path = os.path.join(prompt_dir, f"v{version.version}.json")
        with open(version_path, "w") as f:
            json.dump(version.to_dict(), f, indent=2)

    def commit(
        self, 
        prompt_id: str, 
        commit_message: Optional[str] = None, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[PromptVersion]:
        """Create a new version of a prompt."""
        prompt = self.prompt_manager.get(prompt_id)
        if not prompt:
            return None

        # Initialize versions dict for this prompt if it doesn't exist
        if prompt_id not in self.versions:
            self.versions[prompt_id] = {}
        
        # Get the highest version number for this prompt
        current_versions = self.versions.get(prompt_id, {})
        next_version = max(current_versions.keys(), default=0) + 1
        
        # Create the new version
        version = PromptVersion(
            prompt_id=prompt_id,
            version=next_version,
            content=prompt.content,
            metadata=metadata or {},
            commit_message=commit_message
        )
        
        # Save the new version
        self.versions[prompt_id][next_version] = version
        self._save_version(version)
        
        # Update the prompt's version number
        prompt.version = next_version
        self.prompt_manager._save_prompt(prompt)
        
        return version

    def get_version(self, prompt_id: str, version: int) -> Optional[PromptVersion]:
        """Get a specific version of a prompt."""
        return self.versions.get(prompt_id, {}).get(version)

    def list_versions(self, prompt_id: str) -> List[PromptVersion]:
        """List all versions of a prompt."""
        versions = self.versions.get(prompt_id, {})
        return sorted(versions.values(), key=lambda v: v.version)

    def checkout(self, prompt_id: str, version: int) -> Optional[Prompt]:
        """Checkout a specific version of a prompt."""
        prompt = self.prompt_manager.get(prompt_id)
        version_obj = self.get_version(prompt_id, version)
        
        if not prompt or not version_obj:
            return None
        
        prompt.content = version_obj.content
        prompt.version = version
        prompt.updated_at = datetime.datetime.now().isoformat()
        
        self.prompt_manager._save_prompt(prompt)
        return prompt

    def diff(self, prompt_id: str, version1: int, version2: int) -> Dict[str, Any]:
        """Compare two versions of a prompt."""
        v1 = self.get_version(prompt_id, version1)
        v2 = self.get_version(prompt_id, version2)
        
        if not v1 or not v2:
            return {}
        
        import difflib
        d = difflib.Differ()
        diff = list(d.compare(v1.content.splitlines(), v2.content.splitlines()))
        
        return {
            "version1": version1,
            "version2": version2,
            "diff": diff
        }