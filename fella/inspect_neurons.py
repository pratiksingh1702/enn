import json

with open('fella_checkpoint.json', 'r') as f:
    data = json.load(f)

neurons = data['substrate']['neurons']
print(f"Total Physical Neurons in Manifold: {len(neurons)}")

by_tier = {}
for n in neurons:
    t = n.get('tier_z', 0)
    if t not in by_tier:
        by_tier[t] = []
    by_tier[t].append((n['text'], n.get('role', ''), n.get('grammatical_role', ''), n.get('energy', 0), len(n.get('synapses', {}))))

for t in sorted(by_tier.keys()):
    print(f"\n=======================================================")
    print(f"=== TIER Z = {t} (Total Nodes: {len(by_tier[t])}) ===")
    print(f"=======================================================")
    items = sorted(by_tier[t], key=lambda x: x[4], reverse=True)
    for text, role, gram_role, energy, syn_count in items:
        print(f"  • [{text}] | role: {role} | grammar: {gram_role} | Energy: {energy:.2f} | Synapses (W_ij): {syn_count}")

# Check sample synaptic connections
print("\n=== SAMPLE SYNAPTIC PATHWAYS (W_ij Conductance) ===")
neuron_map = {n['id']: n for n in neurons}
text_map = {n['text']: n for n in neurons}

sample_concepts = ['sun', 'water', 'plants', 'gravity', 'fire', 'fella', 'who', 'why', 'where', 'how']
for sc in sample_concepts:
    if sc in text_map:
        node = text_map[sc]
        top_syns = sorted(node['synapses'].items(), key=lambda kv: float(kv[1]), reverse=True)[:6]
        syn_str = ", ".join([f"{neuron_map.get(int(dst_id), {}).get('text', '?')} (W={float(w):.2f})" for dst_id, w in top_syns])
        print(f"\nNode [{sc}] (Z={node['tier_z']}):")
        print(f"  Connected to: {syn_str}")
