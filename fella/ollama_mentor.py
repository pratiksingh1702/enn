"""
FELLA Ollama Mentor: Trait-Filtered Relational Knowledge Distillation
====================================================================
Queries local Ollama (http://127.0.0.1:11434) and distills raw explanations
into core relational assertions ([Subject] -> [Relation] -> [Object/Property])
to be directly integrated into existing concept networks.
"""

import urllib.request
import urllib.error
import json
import re
import time
from typing import Dict, Any, List, Optional
from fella.metacognition import EpistemicVacuum


class OllamaMentor:
    """
    Interface to the local Ollama LLM mentor.
    Acts as the external world / library for FELLA's curiosity loop.
    """
    def __init__(self, base_url: str = "http://127.0.0.1:11434", default_model: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.preferred_model = default_model
        self.active_model: str = "llama3.2:latest"
        self.is_online: bool = False
        self._check_availability()

    def _check_availability(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", headers={"User-Agent": "FELLA-Agent/1.0"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                if models:
                    if self.preferred_model and self.preferred_model in models:
                        self.active_model = self.preferred_model
                    elif "llama3.2:latest" in models:
                        self.active_model = "llama3.2:latest"
                    elif "qwen2.5:3b" in models:
                        self.active_model = "qwen2.5:3b"
                    else:
                        self.active_model = models[0]
                    self.is_online = True
                    return True
        except Exception:
            self.is_online = False
        return False

    def query_mentor(self, prompt: str, timeout: float = 15.0) -> str:
        if not self.is_online:
            self._check_availability()
            
        if not self.is_online:
            return ""
            
        try:
            payload = {
                "model": self.active_model,
                "prompt": prompt,
                "system": (
                    "You are a scientific and clear mentor to a cognitive AI named FELLA. "
                    "State the core properties, cause-and-effect relationships, and physical principles in 2 clear sentences. "
                    "Use precise subject-action-object relational facts."
                ),
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 100
                }
            }
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                return res_json.get("response", "").strip()
        except Exception:
            return ""

    def ask_about_vacuum(self, vacuum: EpistemicVacuum) -> Dict[str, Any]:
        concept = vacuum.concept_query
        prompt = f"Explain what '{concept}' is, its primary cause, and what it produces or affects in nature."
        if vacuum.context_prompt:
            prompt += f" Context: {vacuum.context_prompt}."
            
        raw_explanation = self.query_mentor(prompt)
        
        return {
            "vacuum_id": vacuum.vacuum_id,
            "concept": concept,
            "prompt_asked": prompt,
            "mentor_model": self.active_model if self.is_online else "offline",
            "explanation": raw_explanation
        }
