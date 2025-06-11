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

def plot_two_las(injector, well, label1="Curve 1", label2="Curve 2", title_name="Title"):
    plt.figure(figsize=(8, 12))  # Taller plot since DEPT is vertical

    GR1, DEPT1 = injector['GR'], injector['DEPT']
    GR2, DEPT2 = well['GR'], well['DEPT']

    plt.plot(GR1, DEPT1, label=label1, color='blue')
    plt.plot(GR2, DEPT2, label=label2, color='green')

    plt.gca().invert_yaxis()  # Depth should increase downward
    plt.xlabel("GR")
    plt.ylabel("DEPT")
    plt.title(title_name)
    plt.ylim(top=1000)
    plt.xlim(left=-1)
    plt.grid(True)
    plt.legend()
    plt.savefig('graphs\my_plot.png')
    plt.show()



def print_k_shifting(k_values, distances, maximum = True, title_name = "Title"):
    plt.figure(figsize=(10, 5))
    plt.plot(k_values, distances, marker='o', linestyle='-')
    plt.title(title_name)
    plt.xlabel("Shift k")
    plt.ylabel("Euclidean Distance")
    plt.grid(True)
    if maximum:
        plt.axvline(x=k_values[distances.index(max(distances))], color='red', linestyle='--', label='Min Distance')
    else:
        plt.axvline(x=k_values[distances.index(min(distances))], color='red', linestyle='--', label='Min Distance')
    plt.xlim(left=-51, right=51)
    plt.legend()
    plt.show()

def clear_plots():
    plt.close('all')