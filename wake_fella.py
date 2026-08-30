import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain
from fella.sensory_bridge import MultimodalSensoryBridge

def wake_fella():
    print("===============================================================")
    print("🧠 WAKING FELLA (536D Multimodal State)")
    print("===============================================================")
    
    if not os.path.exists("fella_checkpoint.json"):
        print("Error: Could not find fella_checkpoint.json. Did you run the Phase 3 training?")
        return

    # Load Brain and Sensory Bridge
    brain = FellaBrain.load_state("fella_checkpoint.json")
    bridge = MultimodalSensoryBridge(substrate_dim=brain.substrate.dim, input_dim=536)
    
    print(f"✓ Neural Core Online ({len(brain.substrate.neurons)} Living Neurons)")
    print("✓ Visual & Physics Cortex Attached")
    print("Type 'exit' to sleep.")
    print("---------------------------------------------------------------\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'sleep']:
                print("FELLA is going to sleep. Goodbye!")
                break
                
            if not user_input.strip():
                continue

            # 1. Talk to her (Text traversal)
            telemetry = brain.converse(user_input)
            response = telemetry.get('last_response', 'uncertainty')
            print(f"\nFELLA: {response}")

            # 2. Extract her Sensory Imagination
            # We find the node with the highest energy currently in her mind
            active_nodes = [n for n in brain.substrate.neurons.values() if n.energy > 0.1]
            if active_nodes:
                # Sort by energy to find the dominant thought
                dominant_node = sorted(active_nodes, key=lambda x: x.energy, reverse=True)[0]
                
                # Decode the 16D substrate vector back into 536D reality
                imagined = bridge.decode_sensory_imagination(dominant_node.x)
                
                print(f"   [Internal Sensory State for '{dominant_node.text.upper()}']:")
                print(f"   👁️ Mental Eye : Optical Resonance = {imagined.visual.mean():.4f}")
                print(f"   🔥 Physics    : Temp log10(T) = {imagined.physics[0]:.2f}")
                print(f"   ❤️ Emotion    : Valence = {imagined.emotion[0]:.2f} | Warmth = {imagined.emotion[3]:.2f}")
            else:
                print("   [Internal Sensory State: Blank / Void]")
            
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\nFELLA forced to sleep.")
            break
        except Exception as e:
            print(f"\n[Cognitive Error]: {e}")

if __name__ == "__main__":
    wake_fella()
