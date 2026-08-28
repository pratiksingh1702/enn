import sys
import io
import json
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def analyze_body_evolution():
    state = json.loads(urllib.request.urlopen('http://127.0.0.1:8765/api/live_state').read().decode('utf-8'))
    org = state['organism']
    
    print("================================================================================")
    print("SOMATIC BODY EVOLUTION & MORPHOGENESIS REPORT")
    print("================================================================================")
    print(f"Step: {state['step']} | Running Time: {state['elapsed_sec']}s | Action: {org['outcome']}")
    print(f"Total Morphogenesis Transformations: {org['cells_morphed']}")
    print(f"Bipedal Steps Walked: {org['steps_walked']}")
    print(f"Energy: {org['energy']} | Free Ether: {org['ether_harvested']} | Walls Built: {org['structures_built']}")
    print(f"Active Curiosity Focus: {org.get('curiosity_focus', 'N/A')}")
    print("-" * 80)
    print("ANATOMICAL LIMB SCHEMA & MASTERY BREAKDOWN:")
    for limb in org['anatomy']:
        mastery_pct = int(limb['mastery'] * 100)
        bar = "█" * (mastery_pct // 5) + "░" * (20 - mastery_pct // 5)
        print(f"  • {limb['name']:<12} [{limb['type']:<11}] Mastery: {mastery_pct:>3}% [{bar}] | Status: {limb['status']}")
    print("-" * 80)
    print("ENN 4D BRAIN SUBSTRATE EVOLUTION:")
    enn = org['enn_metrics']
    print(f"  • Total 4D Neurons Born:   {enn['neurons_born_total']}")
    print(f"  • Active Synaptic Bridges: {enn['synapses_active']}")
    print(f"  • Active Trait Basin:      {enn['active_basin']}")
    print(f"  • Trait Forces:            {enn['trait_pulls']}")
    print("================================================================================")

if __name__ == "__main__":
    analyze_body_evolution()
