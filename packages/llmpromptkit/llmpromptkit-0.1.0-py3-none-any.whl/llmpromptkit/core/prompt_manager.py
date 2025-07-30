import os
import json
import hashlib
import datetime
from typing import Dict, List, Optional, Union, Any

class Prompt:
    def __init__(
        self,
        content: str,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.content = content
        self.name = name
        self.description = description or ""
        self.tags = tags or []
        self.metadata = metadata or {}
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = self.created_at
        self.id = self._generate_id()
        self.version = 1

    def _generate_id(self) -> str:
        """Generate a unique ID based on content and name."""
        unique_string = f"{self.name}:{self.content}:{self.created_at}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:10]

    def update(self, content: Optional[str] = None, **kwargs) -> None:
        """Update prompt attributes."""
        if content is not None:
            self.content = content
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert prompt to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prompt":
        """Create prompt from dictionary."""
        prompt = cls(
            content=data["content"],
            name=data["name"],
            description=data.get("description", ""),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {})
        )
        prompt.id = data["id"]
        prompt.created_at = data["created_at"]
        prompt.updated_at = data["updated_at"]
        prompt.version = data["version"]
        return prompt

    def render(self, **kwargs) -> str:
        """Render prompt with provided variables."""
        rendered = self.content
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            rendered = rendered.replace(placeholder, str(value))
        return rendered


class PromptManager:
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.path.join(os.getcwd(), "llmpromptkit_storage")
        self.prompts: Dict[str, Prompt] = {}
        self._ensure_storage_dir()
        self._load_prompts()

    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists."""
        os.makedirs(self.storage_path, exist_ok=True)

    def _load_prompts(self) -> None:
        """Load prompts from storage."""
        prompts_dir = os.path.join(self.storage_path, "prompts")
        if not os.path.exists(prompts_dir):
            os.makedirs(prompts_dir)
            return

        for filename in os.listdir(prompts_dir):
            if filename.endswith(".json"):
                with open(os.path.join(prompts_dir, filename), "r") as f:
                    prompt_data = json.load(f)
                    prompt = Prompt.from_dict(prompt_data)
                    self.prompts[prompt.id] = prompt

    def _save_prompt(self, prompt: Prompt) -> None:
        """Save prompt to storage."""
        prompts_dir = os.path.join(self.storage_path, "prompts")
        os.makedirs(prompts_dir, exist_ok=True)
        
        prompt_path = os.path.join(prompts_dir, f"{prompt.id}.json")
        with open(prompt_path, "w") as f:
            json.dump(prompt.to_dict(), f, indent=2)

    def create(
        self,
        content: str,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Prompt:
        """Create a new prompt."""
        prompt = Prompt(
            content=content,
            name=name,
            description=description,
            tags=tags,
            metadata=metadata
        )
        self.prompts[prompt.id] = prompt
        self._save_prompt(prompt)
        return prompt

    def get(self, prompt_id: str) -> Optional[Prompt]:
        """Get prompt by ID."""
        return self.prompts.get(prompt_id)

    def update(self, prompt_id: str, **kwargs) -> Optional[Prompt]:
        """Update prompt by ID."""
        prompt = self.get(prompt_id)
        if prompt:
            prompt.update(**kwargs)
            self._save_prompt(prompt)
        return prompt

    def delete(self, prompt_id: str) -> bool:
        """Delete prompt by ID."""
        if prompt_id in self.prompts:
            del self.prompts[prompt_id]
            prompt_path = os.path.join(self.storage_path, "prompts", f"{prompt_id}.json")
            if os.path.exists(prompt_path):
                os.remove(prompt_path)
            return True
        return False

    def list(self, tags: Optional[List[str]] = None) -> List[Prompt]:
        """List prompts, optionally filtered by tags."""
        if tags:
            return [p for p in self.prompts.values() if any(tag in p.tags for tag in tags)]
        return list(self.prompts.values())

    def search(self, query: str) -> List[Prompt]:
        """Search prompts by name or content."""
        query = query.lower()
        return [
            p for p in self.prompts.values() 
            if query in p.name.lower() or query in p.content.lower()
        ]