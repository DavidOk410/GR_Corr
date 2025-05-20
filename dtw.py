from matplotlib.patches import ConnectionPatch
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import scipy.spatial.distance as dist
from matplotlib import cm


def dp(dist_mat):
    """
    Find minimum-cost path through matrix `dist_mat` using dynamic programming.

    The cost of a path is defined as the sum of the matrix entries on that
    path. See the following for details of the algorithm:

    - http://en.wikipedia.org/wiki/Dynamic_time_warping
    - https://www.ee.columbia.edu/~dpwe/resources/matlab/dtw/dp.m

    The notation in the first reference was followed, while Dan Ellis's code
    (second reference) was used to check for correctness. Returns a list of
    path indices and the cost matrix.
    """

    N, M = dist_mat.shape

    # Initialize the cost matrix
    cost_mat = np.zeros((N + 1, M + 1))
    for i in range(1, N + 1):
        cost_mat[i, 0] = np.inf
    for i in range(1, M + 1):
        cost_mat[0, i] = np.inf

    # Fill the cost matrix while keeping traceback information
    traceback_mat = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            penalty = [
                cost_mat[i, j],  # match (0)
                cost_mat[i, j + 1],  # insertion (1)
                cost_mat[i + 1, j]]  # deletion (2)
            i_penalty = np.argmin(penalty)
            cost_mat[i + 1, j + 1] = dist_mat[i, j] + penalty[i_penalty]
            traceback_mat[i, j] = i_penalty

    # Traceback from bottom right
    i = N - 1
    j = M - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        tb_type = traceback_mat[i, j]
        if tb_type == 0:
            # Match
            i = i - 1
            j = j - 1
        elif tb_type == 1:
            # Insertion
            i = i - 1
        elif tb_type == 2:
            # Deletion
            j = j - 1
        path.append((i, j))

    # Strip infinity edges from cost_mat before returning
    cost_mat = cost_mat[1:, 1:]
    return (path[::-1], cost_mat)

def normalize_median(data):
    arr = np.array(data)
    median = np.median(arr)
    result = arr - median
    return result

def normalize_mode(data):
    arr = np.array(data)
    mode = stats.mode(arr, keepdims=False).mode  # mode returns an object, so we extract .mode
    result = arr - mode
    return result

x = np.array([51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 80, 51, 100, 51, 70, 80, 150])
y = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 20, 40, 50, 10, 70, 80, 70, 80, 70, 80, 110])

x_median = normalize_mode(x)
y_median = normalize_mode(y)

plt.figure(figsize=(6, 4))
plt.plot(np.arange(x_median.shape[0]) + 1, x_median + 1.5, "-o", c="C3")
plt.plot(np.arange(y_median.shape[0]) + 1, y_median - 1.5, "-o", c="C0")
plt.axis("off")
plt.show()

# Distance matrix
N = x_median.shape[0]
M = y_median.shape[0]
dist_mat = np.zeros((N, M))
for i in range(N):
    for j in range(M):
        dist_mat[i, j] = abs(x_median[i] - y_median[j])

# DTW
path, cost_mat = dp(dist_mat)

# Plot alignment
plt.figure(figsize=(6, 4))
for x_i, y_j in path:
    plt.plot([x_i, y_j], [x_median[x_i] + 1.5, y_median[y_j] - 1.5], c="C7")
plt.plot(np.arange(x_median.shape[0]), x_median + 1.5, "-o", c="C3")
plt.plot(np.arange(y_median.shape[0]), y_median - 1.5, "-o", c="C0")
plt.axis("off")
plt.show()

plt.figure(figsize=(6, 4))
plt.imshow(cost_mat, cmap=plt.cm.binary, interpolation="nearest", origin="lower")
x_path, y_path = zip(*path)
plt.plot(y_path, x_path)
plt.xlabel("$j$")
plt.ylabel("$i$")

path, cost_mat = dp(dist_mat)
print("Alignment cost: {:.4f}".format(cost_mat[N - 1, M - 1]))
print("Normalized alignment cost: {:.4f}".format(cost_mat[N - 1, M - 1]/(N + M)))


def r2_score_correlation(wells):
    record_plots = []
    for i in range(len(wells) - 1):
        min_distance = -9999
        record_k = 0
        avg_distance = min_distance

        k_graph = []
        for k in range(-50, 51):
            moved_wells = las.wells_shifted(wells, k)
            cutted = las.cut_depth_wells(moved_wells)
            cutted_to_np = las.cutted_to_np(cutted)
            distance = sk.metrics.r2_score(cutted_to_np[0], cutted_to_np[i + 1])
            k_graph.append(distance)
            if distance > min_distance:
                min_distance = distance
                record_k = k
        percentage = 1 / math.exp(min_distance) * 100
        plots.print_k_shifting(range(-50, 51), k_graph)
        print(f"Minimum distance {min_distance:.4f} at value {record_k} (lower = more similar)")
        min_distance_plot = las.cut_depth_wells(las.wells_shifted(wells, record_k))[i + 1]
        record_plots.append(min_distance_plot)
    return record_plots
