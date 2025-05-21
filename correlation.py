
from scipy.signal import correlate
import numpy as np
import las_files as las
import sklearn as sk
import plots
import math
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

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


def normalized_cross_correlation(x, y):
    x = (x - np.mean(x)) / (np.std(x) + 1e-10)
    y = (y - np.mean(y)) / (np.std(y) + 1e-10)

    corr = np.correlate(x, y, mode='full')
    corr /= len(x)  # Normalize by signal length (optional)

    lags = np.arange(-len(x) + 1, len(x))
    print(np.mean(lags))
    best_lag = lags[np.argmax(corr)]
    best_corr = np.max(corr)

    return best_lag, corr

def dtw_distance_correlation(wells):
    record_plots = []
    for i in range(len(wells) - 1):
        min_distance = float('inf')
        record_k = 0
        k_graph = []

        for k in range(-50, 51):
            moved_wells = las.wells_shifted(wells, k)
            cutted = las.cut_depth_wells(moved_wells)
            cutted_to_np = las.cutted_to_np(cutted)
            print(cutted_to_np, cutted_to_np[0], cutted_to_np[i + 1])
            distance, _ = fastdtw(cutted_to_np[0], cutted_to_np[i + 1])
            k_graph.append(distance)

            if distance < min_distance:
                min_distance = distance
                record_k = k

        similarity_score = 1 / (1 + min_distance) * 100  # convert to similarity-like %
        plots.print_k_shifting(range(-50, 51), k_graph)

        print(f"Minimum DTW distance {min_distance:.4f} at k={record_k} (lower = more similar)")
        print(f"Similarity: {similarity_score:.2f}%")

        best_plot = las.cut_depth_wells(las.wells_shifted(wells, record_k))[i + 1]
        record_plots.append(best_plot)

    return record_plots