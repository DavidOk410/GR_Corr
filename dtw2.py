from fastdtw import fastdtw
import numpy as np
import las_files as las
import parsing as pars
import correlation as corr
from scipy.spatial.distance import euclidean

injector = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_7276_inj.las")
well3894 = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_3894.las", False, injector)
well8480 = pars.parse_transformation("D:\Python\Abai\\1 cell\GR_8480.las", False, injector)

print(injector.head(), well3894.head())

wells = [injector, well3894, well8480]
for i in range(len(wells) - 1):
    min_distance = float('inf')
    record_k = 0
    k_graph = []
    for k in range(-50, 51):
        moved_wells = las.wells_shifted(wells, 10)
        cutted = las.cut_depth_wells(moved_wells)
        cutted_to_np = las.cutted_to_np(cutted)

        x = cutted_to_np[0]
        y = cutted_to_np[i+1]
        print(x.shape)
        distance, _ = fastdtw(x, y)
        print(distance)