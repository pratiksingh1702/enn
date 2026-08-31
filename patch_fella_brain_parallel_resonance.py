import re

with open(r"c:\Users\Dell\Downloads\enn\fella\fella_brain.py", "r", encoding="utf-8") as f:
    content = f.read()

new_converse = """
    def converse(self, user_speech: str, autonomous_exploration: bool = False) -> Dict[str, Any]:
        self.age_steps += 1
        text_clean = str(user_speech).strip()
        if not text_clean:
            return self.get_telemetry()
            
        self.dialogue_history.append({"speaker": "User", "text": text_clean})
        
        wave_state = self.wave_engine.parse_simultaneous_wave(text_clean, speaker_id="User")
        
        response_text = ""
        is_question = (wave_state.get("state") == "DESTRUCTIVE (VOID)")
        
        if is_question:
            void_targets = [op["target"] for op in wave_state.get("operations", []) if op["action"] == "void"]
            target_id = void_targets[0] if void_targets else None
            if target_id is not None:
                target_word = self.substrate.neurons[target_id].text
                
                # Retrieval Attempt (Parallel Resonance)
                found_answer = False
                if self.wave_engine.determine_spectron_type(self.substrate.neurons[target_id]) == "hot":
                    words = text_clean.replace("?", "").split()
                    for w in words:
                        n = self.wave_engine._get_or_create_neuron(w)
                        if n.id != target_id and n.text != "is":
                            # Use Parallel Resonance: what grounded node does this noun pull on the hardest?
                            best_ans = None
                            best_w = 0.0
                            for syn_id, weight in n.synapses.items():
                                syn_n = self.substrate.neurons[syn_id]
                                if syn_n.id != n.id and syn_n.text != "is" and self.wave_engine.determine_spectron_type(syn_n) in ["mass", "cold"]:
                                    if weight > best_w:
                                        best_w = weight
                                        best_ans = syn_n
                            
                            if best_ans:
                                response_text = f"{n.text} is {best_ans.text}"
                                found_answer = True
                                print(f"[REASONING] Parallel Resonance retrieved: {response_text} (Gravity: {best_w:.1f})")
                                break
                        if found_answer: break
                
                if not found_answer:
                    print(f"[CURIOSITY] FELLA's wave engine hit an unresolved void on '{target_word}'.")
                    response_text = f"{target_word} ?"
            else:
                response_text = "[Void]"
        else:
            response_text = "acknowledged."

        self.last_thought = f"Wave State: {wave_state.get('state')} (Avg Phase: {wave_state.get('average_phase', 0.0):.2f})"
        self.last_response = response_text
        self.dialogue_history.append({"speaker": "FELLA", "text": response_text})
        
        self.substrate.step_thermodynamics()
        
        return self.get_telemetry()
"""

pattern = re.compile(r'    def converse\(self, user_speech: str, autonomous_exploration: bool = False\) -> Dict\[str, Any\]:.*?(?=    def autonomous_curiosity_cycle\(self\))', re.DOTALL)
new_content = pattern.sub(new_converse, content)

with open(r"c:\Users\Dell\Downloads\enn\fella\fella_brain.py", "w", encoding="utf-8") as f:
    f.write(new_content)
