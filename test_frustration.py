import numpy as np

def calculate_boltzmann_with_frustration(conductances, alignments, temperature, frustration_weight=2.5):
    """
    H = Resistance (1/C) + lambda * Frustration(1 - alignment)
    """
    resistances = np.array([1.0 / c for c in conductances])
    
    # Frustration = 1.0 - alignment. (0.0 is perfect alignment, 2.0 is total contradiction)
    frustrations = np.array([1.0 - a for a in alignments])
    
    # The New Hamiltonian
    energies = resistances + (frustration_weight * frustrations)
    
    boltzmann_factors = np.exp(-energies / temperature)
    Z = np.sum(boltzmann_factors)
    probs = boltzmann_factors / Z
    
    return energies, probs, resistances, frustrations

def run_frustration_test():
    print("[PATCHED THERMODYNAMIC TEST: The True Cost of Lying]")
    
    options = ["Blind (Popular Lie)", "Echolocate (Rare Truth)"]
    conductances = [10.0, 2.0]  # Frequency (Hebbian learning)
    
    # The new mechanism: Alignment with the Tier 3 Causal Vector
    # "Blind" contradicts the causal reality of the bat (-0.5 alignment)
    # "Echolocate" aligns perfectly with the causal reality (0.9 alignment)
    alignments = [-0.5, 0.9]
    
    print("\nTarget Concept: 'Bats'")
    for opt, c, a in zip(options, conductances, alignments):
        print(f" -> Edge: '{opt}' | Frequency: {c:4.1f} | Causal Alignment: {a:4.1f}")
    print("-" * 65)
    
    temperatures = [10.0, 5.0, 1.0, 0.5, 0.1, 0.01]
    
    for T in temperatures:
        energies, probs, res, frust = calculate_boltzmann_with_frustration(conductances, alignments, T)
        print(f"Temperature (T) = {T:5.2f}")
        for opt, E, P, R, F in zip(options, energies, probs, res, frust):
            print(f"  [{opt[:10]}...] Total Energy: {E:5.2f}J (Res: {R:4.2f}, Frust: {F:4.2f}) | Prob: {P*100:5.2f}%")
        print("-" * 65)

if __name__ == '__main__':
    run_frustration_test()
