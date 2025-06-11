import parsing as pars
from pathlib import Path

path = "D:\Python\GR_Corr\\cell 1\INJ_7276.las"
x = Path(path)
print(x.stem)


def transform_cell(wells_paths):
    # Разбиение на окна
    wells = []
    wells_name = []
    for i, well in enumerate(wells_paths):
        if i == 0:
            wells.append(pars.parse_transformation(well))
            wells_name.append(Path(well).stem)
        else:
            wells.append(pars.parse_transformation(well, False, wells[0]))
            wells_name.append(Path(well).stem)
    print(wells_name)
    return wells, wells_name

