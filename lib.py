import os
import random
import numpy as np
from collections import deque
import typing as typ
import pandas as pd

def bucket(
        dataset: np.ndarray, 
        num_buckets: int, 
        range: typ.Union[typ.Tuple[int, int], list[int]] = (0, 1)
    ) -> np.ndarray:
    '''
    Bucket dataset into num_buckets, assumes layer of dataset to bucket on is final 
    (i.e. if dataset.shape = (19, 240, 1000), will bucket into (19, 240, num_buckets)).

    range is exclusive on the right except the last bucket which is inclusive on both sides
    '''
    spacer = (range[1] - range[0]) / num_buckets
    return np.apply_along_axis(
        lambda x: np.histogram(
            x, 
            bins=np.arange(
                range[0], 
                range[1] + spacer, 
                spacer
            )
        )[0],
        len(dataset.shape) - 1,
        dataset
    )

def rotate(
        arr: np.ndarray, 
        num: int
    ) -> np.ndarray:
    '''
    Rotate the ordering of the indices of arr
    '''
    ind = deque(np.arange(0, len(arr.shape)))
    ind.rotate(num)
    return np.transpose(arr, ind)


def data_reader(
        fname: str,
        names: list[str] = [],
        exts: list[str] = []):
    '''
    Read in data from file.
    Appends file names and extensions to names and exts repectively if specified.
    '''
    _fname, fext = os.path.splitext(fname)
    names.append(_fname)
    exts.append(fext)
    
    if fext == ".npy":
        return np.load(fname)
    
    elif fext == ".csv":
        data = np.loadtxt(fname, delimiter=",")
        return data

def random_unique_permutations(
        arr: typ.MutableSequence, 
        max_choices: int = -2
    ) -> typ.Generator[typ.MutableSequence, None, None]:
    '''
    Generate random, unique permutations of arr upto max_choices number of values.
    WILL enter infinite loop if called more than len(arr)! times. We do NOT check for this.
    '''
    max_choices += 1
    prev_permutations = []
    while True:
        random.shuffle(arr)
        new_permutation = arr[:max_choices]
        while new_permutation in prev_permutations:
            random.shuffle(arr)
            new_permutation = arr[:max_choices]

        yield new_permutation


def match(
        arr: typ.Sequence
    ) -> bool:
    '''
    Check if all in `arr` are the same value
    '''
    first = arr[0]
    for item in arr:
        if first != item:
            return False
    return True
