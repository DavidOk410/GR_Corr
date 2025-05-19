
import math
from scipy.spatial.distance import euclidean


import las_files as las
import parsing as pars
import plots
import sklearn as sk
import matplotlib.pyplot as plt

window_size = 200
window_step = 100 #15 fits the best


# Разбиение на окна

injector = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_7276_inj.las")
well3894 = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_3894.las", False, injector)
well8480 = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_8480.las", False, injector)
well24402 = pars.parse_transformation("D:\Python\Abai\\2 cell\GR_24402.las", False, injector)
well2389 = pars.parse_transformation("D:\Python\Abai\\2 cell\GR_2389.las", False, injector)

plots.clear_plots()
plt.clf()     # Clears the current figure
plt.cla()     # Clears the current axes
plt.close()

wells = [injector, well3894, well8480, well24402, well2389]
record_plots = []
for i in range(len(wells) - 1):
    min_distance = -9999
    record_k = 0
    avg_distance = min_distance
    k_graph = []
    for k in range(-50, 51):
        moved_wells = las.move_wells(wells, k)
        cutted = las.cut_depth_wells(moved_wells)
        cutted_to_np = las.cutted_to_np(cutted)
        distance = sk.metrics.r2_score(cutted_to_np[0], cutted_to_np[i+1])
        k_graph.append(distance)
        if distance > min_distance:
            min_distance = distance
            record_k = k
    percentage = 1 / math.exp(min_distance) * 100
    plots.print_k_shifting(range(-50, 51), k_graph)
    print(f"Minimum distance {min_distance:.4f} at value {record_k} (lower = more similar)")
    min_distance_plot = las.cut_depth_wells(las.move_wells(wells, record_k))[i+1]
    record_plots.append(min_distance_plot)

for well in record_plots:
    plots.print_plot(well["GR"], well["DEPT"])
for well in record_plots:
    plots.plot_two_las(wells[0]['GR'], wells[0]['DEPT'], well["GR"], well["DEPT"])

