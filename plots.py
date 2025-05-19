import matplotlib.pyplot as plt

def print_plot(gr, depth):
    plt.figure(figsize=(6, 10))
    plt.plot(gr, depth, color='green', label='GR')

    plt.gca().invert_yaxis()  # Depth increases downward
    plt.xlabel("Gamma Ray (GR)")
    plt.ylabel("Depth (m)")
    plt.title("Gamma Ray Log")
    plt.grid(True)
    plt.legend()

    max_gr = max(gr)
    plt.xlim(left=0, right=max_gr + 10)

    plt.tight_layout()
    plt.show()

def print_k_shifting(k_values, distances, well_name="Well"):
    plt.figure(figsize=(10, 5))
    plt.plot(k_values, distances, marker='o', linestyle='-')
    plt.title(f"Euclidean Distance vs Shift (k) for {well_name}")
    plt.xlabel("Shift k")
    plt.ylabel("Euclidean Distance")
    plt.grid(True)
    plt.axvline(x=k_values[distances.index(min(distances))], color='red', linestyle='--', label='Min Distance')
    plt.legend()
    plt.show()