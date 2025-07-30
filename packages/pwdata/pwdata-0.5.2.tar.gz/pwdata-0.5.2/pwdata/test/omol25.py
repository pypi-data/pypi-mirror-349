import numpy as np
import os, glob
from tqdm import tqdm
from pwdata.image import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from collections import Counter
from functools import partial
from pwdata.fairchem.datasets.ase_datasets import AseDBDataset
from pwdata.utils.format_change import to_numpy_array, to_integer, to_float
from pwdata.meta_omol import META_OMol
from pwdata.convert_files import search_by_format
from pwdata.utils.constant import FORMAT, get_atomic_name_from_number, check_atom_type_name

def read_oMol_data(file_list:list[str], atom_names:list[str]=None, query:str=None, cpu_nums:int=1):
    image_list = META_OMol(lmdb_list, atom_names, query, cpu_nums)
    return image_list

if __name__ == "__main__":
    file_list = [
        "/data/home/wuxingxing/codespace/pwdata_dev/examples/omol_data"
    ]
    lmdb_list = []
    for file in file_list:
        _tmp = search_by_format(file, "meta")
        if len(_tmp) > 0:
            lmdb_list.extend(_tmp)
    atom_names = None #["C", "H"]
    query = None
    cpu_nums = 1

    if atom_names is not None:
        try:
            atom_names = get_atomic_name_from_number(atom_names)
        except Exception as e:
            if check_atom_type_name(atom_names):
                pass
            else:
                raise Exception("The input '-t' or '--atom_types': '{}' is not valid, please check the input".format(" ".join(atom_names)))

    image_list = read_oMol_data(lmdb_list, atom_names, query, cpu_nums)
    print(len(image_list))
