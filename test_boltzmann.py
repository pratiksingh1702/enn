import numpy as np

def calculate_boltzmann_probabilities(conductances, temperature):
    """
    Calculates the thermodynamic probability of jumping to each node.
    Hamiltonian H = 1 / Conductance
    P(j) = exp(-H(j) / T) / Z
    """
    # Calculate Hamiltonian (Energy required to cross the edge)
    # Higher conductance = Lower energy barrier
    energies = np.array([1.0 / c for c in conductances])
    
    # Calculate Boltzmann factors
    boltzmann_factors = np.exp(-energies / temperature)
    
    # Partition Function Z (Sum of all states)
    Z = np.sum(boltzmann_factors)
    
    # Probabilities
    probabilities = boltzmann_factors / Z
    return energies, probabilities

def run_empirical_test():
    print("[THERMODYNAMIC ANNEALING TEST: Misconception vs. Truth]")
    
    # Our test case
    options = ["Blind (Popular Misconception)", "Echolocate (Rare Truth)"]
    conductances = [10.0, 2.0]  # Misconception is 5x more frequent
    
    print(f"Target Concept: 'Bats'")
    for opt, c in zip(options, conductances):
        print(f" -> Edge to '{opt}' | Conductance (Frequency): {c}")
    print("-" * 50)
    
    # Annealing schedule (High T to Low T)
    temperatures = [10.0, 5.0, 1.0, 0.5, 0.1, 0.01]
    
    for T in temperatures:
        energies, probs = calculate_boltzmann_probabilities(conductances, T)
        print(f"Temperature (T) = {T:5.2f}")
        for opt, E, P in zip(options, energies, probs):
            print(f"  [{opt}] Energy: {E:.2f} Joules | Probability: {P*100:5.2f}%")
        print("-" * 50)
        
    print("\n[ANALYSIS]")
    print("If the probability converges to 100% on the Misconception at T=0.01,")
    print("the user's critique is mathematically proven correct.")

if __name__ == '__main__':
    run_empirical_test()
