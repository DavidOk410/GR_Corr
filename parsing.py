
import pandas as pd
import numpy as np

import las_files as las

# Разбиение на окна
def create_windows(data: np.ndarray, window_size: int, window_step: int) -> np.ndarray:
    if data.ndim != 1:
        raise ValueError("Input data must be a 1D NumPy array.")
    if window_size > len(data):
        raise ValueError("Window size must be less than or equal to the length of the data.")

    windows = np.lib.stride_tricks.sliding_window_view(data, window_size)
    return windows[::window_step]

def parse_transformation(well, if_inj = True, inj = pd.DataFrame()):
    '''
    No cutting happens in this function, only making LAS-file a DataFrame without NaN values
    :param well: address of LAS-file
    :param if_inj: if it is one
    :return:
    '''
    well = las.las_read_path(well)
    well_compr = well.df().reset_index()[['DEPT', 'GR']]
    if if_inj:
        return well_compr
    if not if_inj:
        multiplier = las.ratio_inj_well(inj, well_compr)
        inj_compr, well_compr = las.apply_multiplier(inj, well_compr, multiplier)
        inj_compr['GR'] = inj_compr['GR'].interpolate(method='linear').fillna(0)
        well_compr['GR'] = well_compr['GR'].interpolate(method='linear').fillna(0)
        return well_compr

def prepare_train_data(wells, injector, window_size, window_step, pos = True):
    '''

    :param wells: array of wells (goes to X1)
    :param injector: injector well (goes as X2)
    :param pos: positive or negative (pos goes to y as 1, neg goes to y as 0)
    :param window_size: size of array used for screening
    :return: X1, X2 and y
    '''

    X2_train = []
    y = []
    for i, well in enumerate(wells):
        X1_train = create_windows(well, window_size, window_step)
        if i == 0:
            X1_train_all = np.array(X1_train)
        else:
            X1_train_all = np.concatenate([X1_train_all, X1_train])
    X2_train = create_windows(injector, window_size, window_step)
    if pos:
        y = np.ones(len(X1_train))
    else:
        y = np.zeros(len(X1_train))
    if len(X1_train) != len(X2_train):
        print("ERROR\nERROR\nLen X1", len(X1_train), "Len X2", len(X2_train))
    else:
        print("SAME SIZE\n Len X1", len(X1_train), "Len X2", len(X2_train))
    return X1_train, X2_train, y

def print_window_size(windows):
    print("Amount of windows:", len(windows))