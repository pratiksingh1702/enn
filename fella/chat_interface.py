"""
FELLA Chat Interface: Interactive Conversational Terminal
=========================================================
Pair programming & developmental conversation interface with FELLA:
- Real-time display of FELLA's internal thought stream
- Trait attractor basin visualization (INQUIRE, ASPIRE, SYNTHESIZE, etc.)
- Epistemic friction and self-confidence gauges
- Commands to trigger curiosity cycles with Ollama or dream consolidation
"""

import sys
import os
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fella.fella_brain import FellaBrain
from fella.trainer import FellaTrainer


def print_banner():
    print("=" * 75)
    print("🌌 FELLA: Continuous (X, Y, Z) Living Language & Cognitive Organism")
    print("   • X-Axis: Sensory Input | Y-Axis: Decoded Output | Z-Axis: Event Stack")
    print("   • Trait Attractors: INQUIRE | ASPIRE | SYNTHESIZE | IDENTITY | CAUTION")
    print("   • Connected to Local Ollama Mentor for Autonomous Self-Education")
    print("=" * 75)
    print("Commands: /curiosity (query Ollama), /dream (consolidate), /planes, /state, /help, /exit\n")


def display_planes(brain: FellaBrain):
    """Displays concept networks grouped along the 5 discrete Z-abstraction tiers."""
    print("\n" + "=" * 70)
    print("📚 FELLA MULTI-NETWORK TIERED (X, Y, Z) COGNITIVE TOPOLOGY")
    print("=" * 70)
    
    tier_titles = {
        0: "TIER Z=0: Graphemic & Phonetic Foundation ('a'..'z')",
        1: "TIER Z=1: Concrete Physical Entity Networks ([sun], [water], [tree]...)",
        2: "TIER Z=2: Functional Action & Property Networks ([warmth], [liquid]...)",
        3: "TIER Z=3: Causal & Scientific Law Networks ([evaporation], [photosynthesis]...)",
        4: "TIER Z=4: Metacognitive, Social & Self-Model Networks ([fella], [friend]...)"
    }
    
    for tier in [4, 3, 2, 1, 0]:
        tier_neurons = [n for n in brain.substrate.neurons.values() if n.tier_z == tier]
        title = tier_titles.get(tier, f"TIER Z={tier}")
        print(f"\n▲ [{title}] — {len(tier_neurons)} Neurons:")
        
        # Group by network_id
        networks = {}
        for n in tier_neurons:
            if n.network_id not in networks:
                networks[n.network_id] = []
            networks[n.network_id].append(n)
            
        for net_id, net_nodes in networks.items():
            node_desc = []
            for n in net_nodes[:6]:
                syn_cnt = len(n.synapses)
                node_desc.append(f"{n.text}(E={n.energy:.1f}, syn={syn_cnt})")
            if len(net_nodes) > 6:
                node_desc.append(f"...(+{len(net_nodes)-6} more)")
            print(f"   • Network '{net_id}': [{', '.join(node_desc)}]")
            
    print("=" * 70 + "\n")


def display_telemetry(brain: FellaBrain):
    """Prints full internal cognitive state."""
    tel = brain.get_telemetry()
    syn = tel["synapse_stats"]
    print("\n" + "=" * 60)
    print(f"🧠 FELLA COGNITIVE TELEMETRY (Age: {tel['age_steps']} steps | Event Z: {tel['current_event_z']:.1f})")
    print("=" * 60)
    print(f"  • Active Trait Basin:    🌟 {tel['active_trait']}")
    print(f"  • Epistemic Friction:    {tel['epistemic_friction']:.3f} | Confidence: {tel['self_confidence']:.3f} (Flow: {tel['flow_state']})")
    print(f"  • Total Living Neurons:  {tel['total_neurons']}")
    print(f"  • Synaptic Bridges:      Total: {syn['total_synapses']} | Intra-Plane: {syn['intra_plane_synapses']} | Cross-Z: {syn['cross_z_inter_plane_synapses']}")
    print(f"  • Active Vacuums:        {tel['active_vacuums']}")
    print(f"  • Ollama Mentor Status:  {'Online (' + tel['ollama_model'] + ')' if tel['ollama_online'] else 'Offline Oracle'}")
    print(f"  • Last Thought:          \"{tel['last_thought']}\"")
    print("=" * 60 + "\n")


def run_chat_session(checkpoint_path: str = "fella_checkpoint.json"):
    print_banner()
    
    # Check if existing checkpoint exists
    if os.path.exists(checkpoint_path):
        print(f"📂 Loading existing FELLA state from {checkpoint_path}...")
        try:
            brain = FellaBrain.load_state(checkpoint_path)
            print(f"✓ Loaded successfully! Total Neurons: {len(brain.substrate.neurons)}")
        except Exception as e:
            print(f"Notice: Could not load ({e}), booting newborn Tabula Rasa brain...")
            brain = FellaBrain(dim=16)
            brain.boot_foundations()
            brain.save_state(checkpoint_path)
    else:
        print("🌱 Booting newborn Tabula Rasa brain for FELLA (Clean Slate)...")
        brain = FellaBrain(dim=16)
        brain.boot_foundations()
        brain.save_state(checkpoint_path)

    print("\n💬 You can now talk to FELLA! Speak naturally as a parent or guide.\n")

    while True:
        try:
            user_input = input("You > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd in ["/exit", "/quit"]:
            brain.save_state(checkpoint_path)
            print(f"💾 Preserved FELLA state to {checkpoint_path}. Goodbye!")
            break
            
        elif cmd in ["/help", "/?"]:
            print("\n[Commands Guide]:")
            print("  /curiosity  - Trigger autonomous inquiry to Ollama mentor")
            print("  /dream      - Run homeostatic wave consolidation & pruning")
            print("  /planes     - Inspect the stacked (X, Y, Z) event planes")
            print("  /state      - View full cognitive telemetry & trait attractors")
            print("  /save       - Save checkpoint to disk")
            print("  /exit       - Save and exit\n")
            continue
            
        elif cmd in ["/state", "/telemetry"]:
            display_telemetry(brain)
            continue
            
        elif cmd == "/planes":
            display_planes(brain)
            continue
            
        elif cmd in ["/curiosity", "/ask"]:
            print("\n🤔 FELLA is reflecting on its epistemic vacuums and querying Ollama...")
            result = brain.autonomous_curiosity_cycle()
            if result:
                tier_z = result.get("tier_z", result.get("new_z_plane", 3))
                print(f"✨ [Learned from {result['mentor_model']}]: \"{result['explanation']}\"")
                print(f"   Integrated onto Tier Z={tier_z} with {result['total_synapses']} synaptic bridges.\n")
            else:
                print("No pending vacuums. Mind is currently in equilibrium.\n")
            continue
            
        elif cmd in ["/dream", "/sleep"]:
            print("\n🌙 FELLA is entering a homeostatic dream state...")
            dream_res = brain.dream_consolidation()
            print(f"✨ Dream Complete! Pruned {dream_res['pruned_synapses']} weak synapses. Confidence restored to {brain.observer.self_confidence:.3f}.\n")
            continue
            
        elif cmd in ["/rehearse", "/practice"]:
            print("\n🔁 FELLA is practicing and fortifying all 26 alphabet letters at Z=0...")
            res = brain.rehearse_letters(practice_rounds=5)
            print(f"✨ Practice Complete! Rehearsed {res['total_letters']} letters across {res['practice_rounds']} cycles (Mean Energy: {res['mean_energy']:.2f}, Intra-Plane Synapses: {res['intra_plane_synapses']}).\n")
            continue
            
        elif cmd == "/save":
            brain.save_state(checkpoint_path)
            print(f"💾 Checkpoint saved to {checkpoint_path}\n")
            continue

        # Normal conversation flow
        brain.converse(user_input)
        tel = brain.get_telemetry()
        
        # Display response with cognitive indicators
        trait_icon = {
            "INQUIRE": "🔍", "ASPIRE": "🚀", "SYNTHESIZE": "🌐",
            "SELF_IDENTITY": "👤", "CAUTION": "🛡️", "AFFIRM": "💚",
            "UNCERTAINTY": "⚖️"
        }.get(tel["active_trait"], "💡")
        
        print(f"\nFELLA [{trait_icon} {tel['active_trait']} | Z={tel['current_event_z']:.1f} | Conf={tel['self_confidence']:.2f}] >")
        print(f"  {tel['last_response']}\n")


if __name__ == "__main__":
    run_chat_session()
