from __future__ import annotations

from copy import deepcopy

import numpy as np
try:
    import cupy as cp
except (ModuleNotFoundError, ImportError):
    import numpy as cp


class _MappedArrayContainer:

    def __init__(self, arr, key_map=None, axis=None):
        breakpoint()
        self.arr = arr

        self.key_map = key_map
        if key_map is not None:
            found_axis = False
            self.num_keys = len(key_map)
            for axis, len_axis in enumerate(list(arr.shape)):
                if len_axis == self.num_keys and not found_axis:
                    self.arr_axis_keys = axis
                    found_axis = True
                    if axis is not None:
                        assert self.arr_axis_keys == axis
                
                elif len_axis == self.num_keys and found_axis:
                    if axis is None:
                        raise ValueError("If your array has two different dimensions with the same length as your keys, this class cannot tell which one you want to use. Must provide axis kwargs.")

                    self.arr_axis_keys = axis

            assert found_axis
            self.forward_key_map = {key: i for i, key in enumerate(key_map)}
            self.reverse_key_map = {i: key for i, key in enumerate(key_map)}

            assert self.arr.shape[self.arr_axis_keys] == self.num_keys 
            self.base_shape = arr.shape
            
            _tmp = list(self.base_shape)
            _tmp.pop(self.arr_axis_keys)
            self.adjust_shape = (self.num_keys,) + tuple(_tmp)

            _tmp2 = list(range(self.ndim))
            _tmp2.pop(self.arr_axis_keys)
            self.forward_transpose = (self.arr_axis_keys,) + tuple(_tmp2)

            _tmp2 = list(range(self.ndim))
            _tmp2[0] = _tmp2[self.arr_axis_keys]
            _tmp2[self.arr_axis_keys] = 0
            self.reverse_transpose = tuple(_tmp2)
            # TODO: better way? take along axis?
            # TODO: need to track axis of interest when tranposes are taken

    @property
    def arr(self):
        return self._arr

    @arr.setter
    def arr(self, arr):
        if hasattr(arr, "get"):  # is cupy
            assert isinstance(arr, cp.ndarray)
            self.use_gpu = True
        else:
            assert isinstance(arr, np.ndarray)
            self.use_gpu = False

        self._arr = arr
        
    def __getitem__(self, index_or_key):
        if self.key_map is None:
            return self.arr[index_or_key]

        if isinstance(index_or_key, str):
            key = index_or_key
            # TODO: take along axis?
            return self.arr.transpose(self.forward_transpose)[self.forward_key_map[key]]

        # elif isinstance(index_or_key, tuple) or isinstance(index_or_key, list):
        #     raise NotImplementedError
        #     index_or_key = list(index_or_key)
            
        #     for i, tmp in enumerate(index_or_key):
        #         if isinstance(tmp, str):
        #             index_or_key[i] = self.forward_index_map[tmp]
        #         elif isinstance(tmp, tuple) or isinstance(tmp, list):
        #             tmp = list(tmp)
        #             for j, tmp2 in enumerate(tmp):
        #                 if isinstance(tmp2, str):
        #                     tmp[j] = self.forward_index_map[tmp2]

        #             index_or_key[i] = np.asarray(tmp, dtype=int)
        #     raise NotImplementedError
        #     return self.arr[index_or_key]

        else:
            return self.arr[index_or_key]

    # TODO: SET ITEM


    @property
    def xp(self):
        xp = np if not self.use_gpu else cp
        return xp

    def __repr__(self):
        breakpoint()
        return f"Need to adjust this: {self.arr}"

    
class NumpyArrayContainer(_MappedArrayContainer, np.ndarray):
    def __new__(cls, arr, *args, **kwargs):
        obj = np.asarray(arr).view(cls)
        return obj

    def to_cupy(self):
        _arr = cp.asarray(self.arr)
        return (CupyArrayContainer(_arr, key_map=self.key, axis=self.axis))

class CupyArrayContainer(_MappedArrayContainer, cp.ndarray):
    def __new__(cls, arr, *args, **kwargs):
        obj = cp.asarray(arr).view(cls)
        return obj

    def to_numpy(self):
        _arr = self.arr.get()
        return (NumpyArrayContainer(_arr, key_map=self.key, axis=self.axis))


def return_x(x):
    return x

class MappedArrayContainer:
    def __new__(cls, arr, *args, name=None, copy=False, **kwargs):
        dc = deepcopy if copy else return_x
        if isinstance(arr, MappedArrayContainer):
            return dc(arr)
        elif isinstance(arr, np.ndarray):
            return NumpyArrayContainer(arr, *args, **kwargs)
        elif isinstance(arr, cp.ndarray):
            return CupyArrayContainer(arr, *args, **kwargs)

    def __array_finalize__(self, obj):
        if obj is None: return
        self.name = getattr(obj, 'name', None)

    def custom_method(self):
        return f"Array name: {self.name}, shape: {self.shape}"
        
        

class Marc(MappedArrayContainer):
    pass


