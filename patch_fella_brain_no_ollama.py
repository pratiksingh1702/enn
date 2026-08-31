import re

with open(r"c:\Users\Dell\Downloads\enn\fella\fella_brain.py", "r", encoding="utf-8") as f:
    content = f.read()

new_converse = """
    def converse(self, user_speech: str, autonomous_exploration: bool = False) -> Dict[str, Any]:
        \"\"\"
        Interactive Conversational Cycle (Pure Wave Physics):
        Passes the input directly into the continuous wave engine.
        \"\"\"
        self.age_steps += 1
        text_clean = str(user_speech).strip()
        if not text_clean:
            return self.get_telemetry()
            
        self.dialogue_history.append({"speaker": "User", "text": text_clean})
        
        # 1. Parse via Pure Wave Physics
        wave_state = self.wave_engine.parse_simultaneous_wave(text_clean, speaker_id="User")
        
        # 2. Formulate Output
        response_text = ""
        is_question = (wave_state.get("state") == "DESTRUCTIVE (VOID)")
        
        if is_question:
            # Epistemic vacuum triggered. 
            void_targets = [op["target"] for op in wave_state.get("operations", []) if op["action"] == "void"]
            target_id = void_targets[0] if void_targets else None
            if target_id:
                target_word = self.substrate.neurons[target_id].text
                print(f"[CURIOSITY] FELLA's wave engine hit a void on '{target_word}'.")
                
                # OLLAMA MENTOR PAUSED. 
                # FELLA relies entirely on the User to teach her. She outputs her vacuum state to prompt the user.
                response_text = f"{target_word} ?"
            else:
                response_text = "[Void]"
        else:
            # Constructive wave. She just grounds it.
            response_text = "acknowledged."

        self.last_thought = f"Wave State: {wave_state.get('state')} (Avg Phase: {wave_state.get('average_phase', 0.0):.2f})"
        self.last_response = response_text
        self.dialogue_history.append({"speaker": "FELLA", "text": response_text})
        
        # 3. Step Thermodynamics
        self.substrate.step_thermodynamics()
        
        return self.get_telemetry()
"""

pattern = re.compile(r'    def converse\(self, user_speech: str, autonomous_exploration: bool = False\) -> Dict\[str, Any\]:.*?(?=    def autonomous_curiosity_cycle\(self\))', re.DOTALL)
new_content = pattern.sub(new_converse, content)

with open(r"c:\Users\Dell\Downloads\enn\fella\fella_brain.py", "w", encoding="utf-8") as f:
    f.write(new_content)
    
print("Successfully paused Ollama and updated converse method.")
