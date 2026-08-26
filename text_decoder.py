"""
Text Decoder for ENN 4D Living Universe
Decodes output Y interference vectors back into human-readable text memories and answers.
"""

import re
import numpy as np
from typing import Dict, Any, List, Optional, Tuple


class TextDecoder:
    """
    Decodes 4D interference output vectors into retrieved text and contextual answers.
    Uses cosine similarity and Euclidean proximity across the living memory log.
    """
    
    def __init__(self, memory_log: Optional[List[Dict[str, Any]]] = None):
        self.memory_log: List[Dict[str, Any]] = memory_log if memory_log is not None else []

    def set_memory_log(self, memory_log: List[Dict[str, Any]]):
        self.memory_log = memory_log

    def compute_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """Computes cosine similarity combined with inverted Euclidean distance."""
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        cosine_sim = float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
        euclid_dist = float(np.linalg.norm(vec_a - vec_b))
        proximity = 1.0 / (1.0 + euclid_dist)
        
        # Blended metric
        return float(0.6 * cosine_sim + 0.4 * proximity)

    def find_nearest_memories(self, y_vector: np.ndarray, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """Finds top-k nearest memories in the memory log to the output Y vector."""
        if not self.memory_log:
            return []
            
        scored = []
        for mem in self.memory_log:
            target_vec = np.array(mem.get('y', mem.get('x')))
            score = self.compute_similarity(y_vector, target_vec)
            scored.append((mem, score))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def format_perspective(self, text: str) -> str:
        """Converts first-person statements to second-person responses."""
        res = text.strip()
        
        # Name patterns
        m_name = re.search(r'\bmy name is\s+(.+)', res, re.IGNORECASE)
        if m_name:
            name = m_name.group(1).rstrip('.!?')
            return f"You are {name}."
            
        m_iam = re.search(r'\bi am\s+(.+)', res, re.IGNORECASE)
        if m_iam:
            fact = m_iam.group(1).rstrip('.!?')
            return f"You are {fact}."
            
        m_like = re.search(r'\bi (like|love|prefer)\s+(.+)', res, re.IGNORECASE)
        if m_like:
            verb = m_like.group(1)
            target = m_like.group(2).rstrip('.!?')
            return f"You {verb} {target}."
            
        # Basic pronoun replacement
        replacements = [
            (r'\bmy\b', 'your'),
            (r'\bmine\b', 'yours'),
            (r'\bi am\b', 'you are'),
            (r'\bi\b', 'you')
        ]
        out = res
        for pat, rep in replacements:
            out = re.sub(pat, rep, out, flags=re.IGNORECASE)
            
        return out if out.endswith(('.', '!', '?')) else out + '.'

    def decode_4d_to_text(
        self, 
        y_vector: np.ndarray, 
        query_text: Optional[str] = None,
        memory_log: Optional[List[Dict[str, Any]]] = None,
        resonance_force: float = 1.0
    ) -> str:
        """
        Decodes output Y vector into natural text.
        Handles both direct statement confirmations and intelligent query answers.
        """
        active_log = memory_log if memory_log is not None else self.memory_log
        
        # Filter declarative memories (statements recorded, not questions)
        declarative_memories = [m for m in active_log if not m.get('is_query', False)]
        if not declarative_memories:
            declarative_memories = active_log

        if not declarative_memories:
            return "My memory field is currently empty."

        clean_query = query_text.strip().lower() if query_text else ""
        is_question = bool(
            clean_query and (
                any(q in clean_query for q in ["what", "who", "where", "why", "how", "tell", "know about me", "?"])
                or clean_query.endswith("?")
            )
        )

        # 1. Multi-memory summary query: "What do you know about me?"
        if "know about me" in clean_query or "everything you know" in clean_query:
            personal_memories = []
            for mem in declarative_memories:
                txt = mem['text']
                if any(w in txt.lower() for w in ["my name", "i am", "i like", "i love", "i live", "i work"]):
                    formatted = self.format_perspective(txt)
                    if formatted not in personal_memories:
                        personal_memories.append(formatted)
                        
            if personal_memories:
                return " ".join(personal_memories)

        # 2. Targeted Query (e.g., "Who am I?", "What is my name?")
        if is_question:
            # Score against declarative memories
            scored = []
            for mem in declarative_memories:
                target_vec = np.array(mem.get('y', mem.get('x')))
                score = self.compute_similarity(y_vector, target_vec)
                
                txt_lower = mem['text'].lower()
                
                # Priority weighting
                if "who am i" in clean_query or "what is my name" in clean_query or "my name" in clean_query:
                    if "my name is" in txt_lower:
                        score += 0.6
                    elif "i am" in txt_lower and not any(w in txt_lower for w in ["scientist", "engineer", "working", "job"]):
                        score += 0.4
                elif "job" in clean_query or "work" in clean_query or "profession" in clean_query or "scientist" in clean_query:
                    if any(w in txt_lower for w in ["scientist", "engineer", "work", "job", "doctor", "teacher"]):
                        score += 0.5
                elif "like" in clean_query or "love" in clean_query or "animal" in clean_query or "pet" in clean_query or "food" in clean_query:
                    if "like" in txt_lower or "love" in txt_lower or "favorite" in txt_lower:
                        score += 0.5
                        
                scored.append((mem, score))
                
            scored.sort(key=lambda x: x[1], reverse=True)
            best_mem, best_score = scored[0]
            
            if "who am i" in clean_query or "what is my name" in clean_query:
                # Find name memory explicitly if present
                for mem in declarative_memories:
                    if "my name is" in mem['text'].lower():
                        m_name = re.search(r'\bmy name is\s+(.+)', mem['text'], re.IGNORECASE)
                        if m_name:
                            return f"You are {m_name.group(1).rstrip('.!?')}."
                return self.format_perspective(best_mem['text'])
                
            return self.format_perspective(best_mem['text'])

        # 3. Declaration confirmation (e.g. user just said "My name is Professor Smith")
        if query_text:
            m_name = re.search(r'\bmy name is\s+(.+)', query_text, re.IGNORECASE)
            if m_name:
                return f"I have recorded your name as {m_name.group(1).rstrip('.!?')}."
                
            m_iam = re.search(r'\bi am\s+(.+)', query_text, re.IGNORECASE)
            if m_iam:
                fact = m_iam.group(1).rstrip('.!?')
                if not (fact.startswith("a ") or fact.startswith("an ") or fact.startswith("the ")):
                    fact = ("an " if fact[0].lower() in "aeiou" else "a ") + fact
                return f"I have recorded that you are {fact}."
                
            m_like = re.search(r'\bi (like|love|prefer)\s+(.+)', query_text, re.IGNORECASE)
            if m_like:
                return f"I have recorded your preference: you {m_like.group(1)} {m_like.group(2).rstrip('.!?')}."

            return f"I have committed this to my living 4D field: '{query_text}'."

        # Fallback: Best nearest memory string
        nearest = self.find_nearest_memories(y_vector, top_k=1)
        if nearest:
            return nearest[0][0]['text']
        return "Resonating in silence."