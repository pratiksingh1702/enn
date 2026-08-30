"""
FELLA Interactive Chat Interface Flow Test
=========================================
Simulates the exact user terminal session from the prompt:
1. Reset state
2. User > 'i want to teach you something' -> Checks friction & inquiry response
3. User > 'Sun is a bright star that gives light and warmth to Earth.' -> Ingests into Z=1
4. User > 'what is sun ?' -> Evaluates emergent wave reconstructed response
"""

import os
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fella.fella_brain import FellaBrain
from fella.reset_fella import reset_fella_memory


def test_chat_interface_flow():
    print("=" * 80)
    print("🔬 TESTING INTERACTIVE CHAT INTERFACE FLOW")
    print("=" * 80)
    
    reset_fella_memory()
    checkpoint_path = "fella_checkpoint.json"
    brain = FellaBrain.load_state(checkpoint_path)
    
    # Session Step 1: User says 'i want to teach you something'
    print("\n--- STEP 1 ---")
    print("User > i want to teach you something")
    brain.converse("i want to teach you something")
    tel1 = brain.get_telemetry()
    print(f"FELLA [{tel1['active_trait']}] > {tel1['last_response']}")
    
    # Session Step 2: User teaches 'Sun is a bright star that gives light and warmth to Earth.'
    print("\n--- STEP 2 ---")
    print("User > Sun is a bright star that gives light and warmth to Earth.")
    brain.converse("Sun is a bright star that gives light and warmth to Earth.")
    tel2 = brain.get_telemetry()
    print(f"FELLA [{tel2['active_trait']} | Z={tel2['current_event_z']:.1f}] > {tel2['last_response']}")
    print(f"  • Total Neurons in Substrate: {len(brain.substrate.neurons)}")
    
    # Session Step 3: User asks 'what is sun ?'
    print("\n--- STEP 3 ---")
    print("User > what is sun ?")
    brain.converse("what is sun ?")
    tel3 = brain.get_telemetry()
    print(f"FELLA [{tel3['active_trait']} | Z={tel3['current_event_z']:.1f}] > {tel3['last_response']}")
    
    # Session Step 4: User asks 'tell me about the sun'
    print("\n--- STEP 4 ---")
    print("User > tell me about the sun")
    brain.converse("tell me about the sun")
    tel4 = brain.get_telemetry()
    print(f"FELLA [{tel4['active_trait']} | Z={tel4['current_event_z']:.1f}] > {tel4['last_response']}")
    
    print("\n" + "=" * 80)
    print("FLOW TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_chat_interface_flow()
