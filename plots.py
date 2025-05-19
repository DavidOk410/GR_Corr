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

def plot_two_las(GR1, DEPT1, GR2, DEPT2, label1="Curve 1", label2="Curve 2"):
    plt.figure(figsize=(8, 12))  # Taller plot since DEPT is vertical

    plt.plot(GR1, DEPT1, label=label1, color='blue')
    plt.plot(GR2, DEPT2, label=label2, color='green')

    plt.gca().invert_yaxis()  # Depth should increase downward
    plt.xlabel("GR")
    plt.ylabel("DEPT")
    plt.title("Comparison of Two GR Curves")
    plt.ylim(top=1000)
    plt.grid(True)
    plt.legend()
    plt.show()



def print_k_shifting(k_values, distances, well_name="Well"):
    plt.figure(figsize=(10, 5))
    plt.plot(k_values, distances, marker='o', linestyle='-')
    plt.title(f"Euclidean Distance vs Shift (k) for {well_name}")
    plt.xlabel("Shift k")
    plt.ylabel("Euclidean Distance")
    plt.grid(True)
    plt.axvline(x=k_values[distances.index(min(distances))], color='red', linestyle='--', label='Min Distance')
    plt.xlim(left=-51, right=51)
    plt.legend()
    plt.show()