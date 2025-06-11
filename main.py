
import math
from scipy.spatial.distance import euclidean


import las_files as las
import parsing as pars
import plots
import correlation as corr
import matplotlib.pyplot as plt
import input as inp

window_size = 200
window_step = 100 #15 fits the best

cell1_paths = ["D:\Python\GR_Corr\\cell 1\INJ_7276.las",
                   "D:\Python\GR_Corr\\cell 1\\1437.las",
                   "D:\Python\GR_Corr\\cell 1\\1666.las",
                   "D:\Python\GR_Corr\\cell 1\\1683.las",
                   "D:\Python\GR_Corr\\cell 1\\1784.las",
                   "D:\Python\GR_Corr\\cell 1\\3668.las",
                   "D:\Python\GR_Corr\\cell 1\\3894.las",
                   "D:\Python\GR_Corr\\cell 1\\4055.las",
                   "D:\Python\GR_Corr\\cell 1\\8384.las",
                   "D:\Python\GR_Corr\\cell 1\\9671.las"]

cell2_paths = ["D:\Python\GR_Corr\\cell 2\\INJ_6838.las",
                   "D:\Python\GR_Corr\\cell 2\\1673.las",
                   "D:\Python\GR_Corr\\cell 2\\1804.las",
                   "D:\Python\GR_Corr\\cell 2\\2389.las",
                   "D:\Python\GR_Corr\\cell 2\\3896.las",
                   "D:\Python\GR_Corr\\cell 2\\7768.las",
                   "D:\Python\GR_Corr\\cell 2\\8435.las",
                   "D:\Python\GR_Corr\\cell 2\\8446.las"]

# Разбиение на окна

chosen_well = [1, 2, 3, 4, 5, 6, 7]


wells, wells_name = inp.transform_cell(cell2_paths)
 #= [all_wells[0], all_wells[chosen_well]]
normalized_wells = las.normalize_ray(wells)
cutted_normalized = las.cut_depth_wells(normalized_wells)
#ill use it for correlations
'''for well in normalized_wells:
    print("NORM WELL", well)'''

#DTW
'''record_plots_DTW = corr.dtw_distance_correlation(normalized_wells)
for i, well in enumerate(record_plots_DTW):
    if i in chosen_well:
        plots.plot_two_las(cutted_normalized[0], well, title_name=f"DTW WELL N{i}")
'''
# R2 SCORE PRINT
record_plots_R2 = corr.r2_score_correlation(normalized_wells)
for i, well in enumerate(record_plots_R2):
    if i in chosen_well:
        plots.plot_two_las(cutted_normalized[0], well, title_name=f"R2_SCORE WELL N{i}")

#Normalized Initial Well
for i, well in enumerate(cutted_normalized):
    if i in chosen_well:
        plots.plot_two_las(cutted_normalized[0], well, title_name=f"Normalized Initial WELL N{i}")

#Simple Initial Well
cutted = las.cut_depth_wells(wells)
for i, well in enumerate(cutted):
    if i in chosen_well:
        plots.plot_two_las(cutted[0], well, title_name=f"Initial WELL N{i}")

'''
# NORMALIZE CROSS CORRELATION
normalized_cutted_to_np = las.cutted_to_np(cutted_normalized)
print(len(normalized_cutted_to_np), normalized_cutted_to_np)
for i, well in enumerate(cutted_normalized):
    if i in chosen_well:
        best_lag, correl = corr.normalized_cross_correlation(normalized_cutted_to_np[0], normalized_cutted_to_np[i])
        print(f"NCC best_lag {best_lag:.4f}")
        best_lag_plot = las.well_shifting(well, best_lag)
        plots.plot_two_las(cutted_normalized[0], best_lag_plot, title_name=f"NCC WELL N{i}")
'''

