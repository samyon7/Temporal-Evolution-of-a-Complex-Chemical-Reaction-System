import numpy as np

def calculate_rate_constants(T, P, catalyst1, catalyst2):
    # Constants
    R = 8.314  # Gas constant in J/(mol*K)
    k1_0 = 1.0  # Pre-exponential factor for Step 1
    k2_0 = 1.0  # Pre-exponential factor for Step 2
    k3_0 = 1.0  # Pre-exponential factor for Step 3
    Ea1 = 50000  # Activation energy for Step 1 in J/mol
    n2 = 0.5  # Power law exponent for pressure dependence of Step 2
    P0 = 1.0  # Reference pressure in atm

    # Calculate temperature-dependent rate constants
    k1 = k1_0 * np.exp(-Ea1 / (R * T))
    k2 = k2_0 * (P / P0) ** n2
    k3 = k3_0
    
    # Apply catalyst effects
    if catalyst1:
        k1 *= 2
    if catalyst2:
        k2 *= 0.5
    
    return k1, k2, k3

def simulate_reaction(initial_concentrations, T, P, catalyst1, catalyst2, dt, n_steps):
    if len(initial_concentrations) != 10:
        raise ValueError("Initial concentrations must be a list of 10 values.")
    
    # Initialize arrays to store concentrations and rates
    concentrations = np.zeros((n_steps + 1, 10))
    rates = np.zeros((n_steps, 3))
    
    # Store initial concentrations
    concentrations[0] = initial_concentrations

    for t in range(n_steps):
        # Unpack current concentrations
        A, B, C, D, E, F, G, H, I, J = concentrations[t]
        
        # Calculate rate constants
        k1, k2, k3 = calculate_rate_constants(T, P, catalyst1, catalyst2)
        
        # Calculate reaction rates
        r1 = k1 * A * B
        r2 = k2 * C * E
        r3 = k3 * F * H
        
        # Store rates
        rates[t] = [r1, r2, r3]
        
        # Update concentrations using Euler method
        dA = -r1 * dt
        dB = -r1 * dt
        dC = r1 * dt - r2 * dt
        dD = r1 * dt
        dE = -r2 * dt
        dF = r2 * dt - r3 * dt
        dG = r2 * dt
        dH = -r3 * dt
        dI = r3 * dt
        dJ = r3 * dt
        
        # Update concentrations
        concentrations[t + 1] = [A + dA, B + dB, C + dC, D + dD, E + dE, F + dF, G + dG, H + dH, I + dI, J + dJ]
    
    return concentrations, rates

def run_simulations(inputs):
    results = []
    for initial_concentrations, T, P, catalyst1, catalyst2, dt, n_steps in inputs:
        concentrations, rates = simulate_reaction(initial_concentrations, T, P, catalyst1, catalyst2, dt, n_steps)
        results.append((concentrations, rates))
    return results

# Custom data inputs (example with multiple simulations)
inputs = [
    ([1.0, 2.0, 0.5, 0.2, 1.5, 0.8, 0.1, 2.5, 0.3, 0.6], 300, 1.0, True, False, 0.01, 100),
    ([1.2, 1.8, 0.6, 0.3, 1.4, 0.9, 0.2, 2.4, 0.4, 0.7], 320, 1.2, False, True, 0.01, 100),
    ([1.1, 1.9, 0.4, 0.1, 1.6, 0.7, 0.3, 2.6, 0.5, 0.8], 310, 1.1, True, True, 0.01, 100),
    # Add more simulations as needed
]

# Run simulations
results = run_simulations(inputs)

# Output the concentrations and rates for each simulation
for i, (concentrations, rates) in enumerate(results):
    print(f"Simulation {i+1}:")
    for t in range(len(concentrations)):
        print(f"Time step {t}: [A]={concentrations[t, 0]:.4f}, [B]={concentrations[t, 1]:.4f}, [C]={concentrations[t, 2]:.4f}, [D]={concentrations[t, 3]:.4f}, [E]={concentrations[t, 4]:.4f}, [F]={concentrations[t, 5]:.4f}, [G]={concentrations[t, 6]:.4f}, [H]={concentrations[t, 7]:.4f}, [I]={concentrations[t, 8]:.4f}, [J]={concentrations[t, 9]:.4f}")
        if t < len(rates):
            print(f"Rate step {t}: r1={rates[t, 0]:.4f}, r2={rates[t, 1]:.4f}, r3={rates[t, 2]:.4f}")
    print("\n" + "-"*80 + "\n")
