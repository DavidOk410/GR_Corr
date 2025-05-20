import lasio
import pandas as pd
import numpy as np

def las_read_path(path):
    pd.set_option('display.max_columns', None)
    las = lasio.read(path)
    return las

def ratio_inj_well(injector, well):
    '''
    input: injectorArray, wellArray (with DEPT and GR attributes)
    compare steps of injector with well
    if injector's step is bigger, cut the well's step
    elif injector's step is smaller, cut the inj's step
    :return true:
    '''
    inj_step = injector['DEPT'][1] - injector['DEPT'][0]
    well_step = well['DEPT'][1] - well['DEPT'][0]
    multiplier = inj_step / well_step
    return int(multiplier)

def apply_multiplier(injector, well, multiplier):
    if multiplier > 1:
        well = compress_well_multiplier(well, multiplier)
    elif 1 > multiplier > 0:
        injector = compress_well_multiplier(injector, multiplier)
    return injector, well

def compress_well_multiplier(well, multiplier):
    well_np = well.to_numpy()
    well_step = well_np[::multiplier]
    df = pd.DataFrame(well_step, columns=['DEPT', 'GR'])
    return df

def well_shifting(well, k = 0):
    moved_well = well.copy()
    moved_well['DEPT'] = moved_well['DEPT'] + k
    return moved_well

def wells_shifted(wells, k = 0):
    moved_wells = [wells[0]]
    for i, well in enumerate(wells):
        if i != 0:
            moved_wells.append(well_shifting(well, k))
    return moved_wells

def cut_depth_wells(wells):
    min_depth = wells[0]['DEPT'].min()
    max_depth = wells[0]['DEPT'].max()
    for well in wells:
        if well['DEPT'].min() > min_depth:
            min_depth = well['DEPT'].min()
        elif well['DEPT'].max() < max_depth:
            max_depth = well['DEPT'].max()
    for i, well in enumerate(wells):
        well_cutted = well[(well['DEPT'] >= 1000) & (well['DEPT'] <= max_depth)]
        wells[i] = well_cutted
    return wells

def cutted_to_np(wells):
    '''
    :param wells: cutted wells in DataFrame format
    :return cutted wells converted to NumPy array:
    '''
    gr_arrays = []
    for well in wells:
        gr_arrays.append(well['GR'].to_numpy())
    return gr_arrays


def well_multiplier(well, required_step):
    '''
    To compress the data for ML learning
    :return multiplier that we need to get required step (1 m, 10 m or more):
    '''
    well_step = well['DEPT'][1] - well['DEPT'][0]
    multiplier = required_step / well_step
    return int(multiplier)