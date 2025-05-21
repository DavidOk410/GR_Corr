
import math
from scipy.spatial.distance import euclidean


import las_files as las
import parsing as pars
import plots
import correlation as corr
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

#DTW Dynamic Time Warping
record_plots = corr.dtw_distance_correlation(wells)
print(len(record_plots))
for i, well in enumerate(record_plots):
    if i == 1:
        plots.plot_two_las(wells[0], well, title_name="DTW")

# R2 SCORE PRINT
record_plots = corr.r2_score_correlation(wells)
print(len(record_plots))
for i, well in enumerate(record_plots):
    if i == 1:
        plots.plot_two_las(wells[0], well, title_name="R2_SCORE")

#NORMALIZE CROSS CORRELATION
cutted = las.cut_depth_wells(wells)
copy = cutted.copy()
plots.plot_two_las(wells[0], copy[2], title_name="Initial") #INITIAL
cutted_to_np = las.cutted_to_np(cutted)
best_lag, corr = corr.normalized_cross_correlation(cutted_to_np[0], cutted_to_np[2])
print(f"lag {best_lag:.4f}")
best_lag_plot = las.well_shifting(cutted[2], best_lag)
plots.plot_two_las(wells[0], best_lag_plot, title_name="NCC")


