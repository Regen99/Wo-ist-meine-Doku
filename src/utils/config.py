import json
import os
from typing import List, Dict

class ConfigManager:
    """
    Handles persistence of user settings and favorite paths.
    Stored in data/config.json.
    """
    def __init__(self, config_path: str = "data/config.json"):
        self.config_path = config_path
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        self.config = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get_favorites(self) -> List[str]:
        return self.config.get("favorite_paths", [])

    def add_favorite(self, path: str):
        favorites = self.get_favorites()
        safe_path = path.replace("\\", "/")
        if safe_path not in favorites:
            favorites.append(safe_path)
            self.config["favorite_paths"] = favorites
            self._save()

    def remove_favorite(self, path: str):
        favorites = self.get_favorites()
        safe_path = path.replace("\\", "/")
        if safe_path in favorites:
            favorites.remove(safe_path)
            self.config["favorite_paths"] = favorites
            self._save()

    def get_last_used_path(self) -> str:
        return self.config.get("last_used_path", "data/raw")

    def set_last_used_path(self, path: str):
        self.config["last_used_path"] = path.replace("\\", "/")
        self._save()
