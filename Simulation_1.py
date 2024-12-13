import numpy as np

# Define constants
R = 8.314  # Gas constant (J/mol·K)
k1_0 = 0.1  # Pre-exponential factor for step 1
Ea1 = 10000  # Activation energy for step 1 (J/mol)
k2_0 = 0.2  # Pre-exponential factor for step 2
P0 = 1  # Reference pressure (atm)
n2 = 0.5 # Pressure exponent for step 2
k3 = 0.3  # Rate constant for step 3

def reaction_simulation(initial_concentrations, T, P, catalyst1, catalyst2, dt, n_steps):
    """Simulates the chemical reaction over multiple time steps.

    Args:
        initial_concentrations (dict): Initial concentrations of all species.
        T (float): Temperature in Kelvin.
        P (float): Pressure in atm.
        catalyst1 (bool): True if catalyst 1 is present, False otherwise.
        catalyst2 (bool): True if catalyst 2 is present, False otherwise.
        dt (float): Time step in seconds.
        n_steps (int): Number of time steps.

    Returns:
        tuple: Lists of concentrations and reaction rates for each time step.
    """
    
    # Make mutable copy of the concentrations
    concentrations = initial_concentrations.copy()
    
    all_concentrations = [concentrations.copy()]
    all_rates = []

    for _ in range(n_steps):
        # Calculate temperature-dependent k1
        k1 = k1_0 * np.exp(-Ea1 / (R * T))

        # Calculate pressure-dependent k2
        k2 = k2_0 * (P / P0) ** n2

        # Apply catalyst effects
        if catalyst1:
            k1 *= 2
        if catalyst2:
            k2 *= 0.5

        # Calculate reaction rates
        r1 = k1 * concentrations["A"] * concentrations["B"]
        r2 = k2 * concentrations["C"] * concentrations["E"]
        r3 = k3 * concentrations["F"] * concentrations["H"]
        
        rates = {"r1": r1, "r2": r2, "r3": r3}
        all_rates.append(rates)

        # Update concentrations based on reaction rates
        concentrations["A"] -= r1 * dt
        concentrations["B"] -= r1 * dt
        concentrations["C"] += r1 * dt - r2 * dt
        concentrations["D"] += r1 * dt
        concentrations["E"] -= r2 * dt
        concentrations["F"] += r2 * dt - r3 * dt
        concentrations["G"] += r2 * dt
        concentrations["H"] -= r3 * dt
        concentrations["I"] += r3 * dt
        concentrations["J"] += r3 * dt
        
        # Ensure we don't have negative concentrations
        for key, value in concentrations.items():
            concentrations[key] = max(0, value)
        
        all_concentrations.append(concentrations.copy())

    return all_concentrations, all_rates

# --- Input Parameters ---
initial_concentrations = {
    "A": 1.0,
    "B": 2.0,
    "C": 0.5,
    "D": 0.2,
    "E": 1.5,
    "F": 0.8,
    "G": 0.1,
    "H": 2.5,
    "I": 0.3,
    "J": 0.6,
}
T = 300  # K
P = 1  # atm
catalyst1 = True
catalyst2 = False
dt = 0.01  # s
n_steps = 100

# --- Run the Simulation ---
all_concentrations, all_rates = reaction_simulation(
    initial_concentrations, T, P, catalyst1, catalyst2, dt, n_steps
)

# --- Output Results ---
print("Time Step\t  A\t  B\t  C\t  D\t  E\t  F\t  G\t  H\t  I\t  J\t   r1\t   r2\t   r3")
for i in range(n_steps + 1):
    c = all_concentrations[i]
    if i < n_steps:
        r = all_rates[i]
        print(
            f"{i * dt:.2f}\t {c['A']:.3f}\t {c['B']:.3f}\t {c['C']:.3f}\t {c['D']:.3f}\t {c['E']:.3f}\t"
            f" {c['F']:.3f}\t {c['G']:.3f}\t {c['H']:.3f}\t {c['I']:.3f}\t {c['J']:.3f}\t"
            f" {r['r1']:.3f}\t {r['r2']:.3f}\t {r['r3']:.3f}"
        )
    else:
        print(
            f"{i * dt:.2f}\t {c['A']:.3f}\t {c['B']:.3f}\t {c['C']:.3f}\t {c['D']:.3f}\t {c['E']:.3f}\t"
            f" {c['F']:.3f}\t {c['G']:.3f}\t {c['H']:.3f}\t {c['I']:.3f}\t {c['J']:.3f}\t"
            f"   -    \t   -    \t   -"
        )
