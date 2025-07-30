import os
import numpy as np
import contextlib
import yaml
import fnmatch
from pathlib import Path
from typing import List, Any, Dict
from ..utils import checklist
from collections import UserDict

_VALID_EXTS = ['.mp3', '.wav', '.aif', '.aiff', '.flac', '.opus']

def audio_paths_from_dir(
        dir_path : str | Path,
        valid_exts: List[str] | None = None, 
        flt: List[str] = [],
        exclude: List[str] = []
    ):
    valid_exts = valid_exts or _VALID_EXTS
    valid_exts = list(map(lambda x: x.lower(), valid_exts)) + list(map(lambda x: x.upper(), valid_exts))
    audio_candidates = []
    base_dir = Path(dir_path)
    flt = checklist(flt)
    exclude = checklist(exclude)
    for ext in valid_exts:
        parsed_candidates = list(map(lambda x: x.resolve(), base_dir.glob(f'**/*{ext}')))
        if len(parsed_candidates) == 0: continue
        if len(flt) > 0:
            filtered_candidates = []
            for f in flt: 
                filtered_candidates.extend(list(filter(lambda x, r = f: fnmatch.fnmatch(x.relative_to(base_dir.absolute()), r), parsed_candidates)))
            parsed_candidates = list(set(filtered_candidates))
        for e in exclude:
            parsed_candidates = list(filter(lambda x, r = e: not fnmatch.fnmatch(x.relative_to(base_dir.absolute()), r), parsed_candidates))
        audio_candidates.extend(map(str, parsed_candidates))
    return audio_candidates 

def read_metadata(path):
    path = Path(path)
    if path.suffix != ".yaml":
        path = path / "metadata.yaml"
    if not path.exists():
        assert FileNotFoundError("yaml file not found for path %s"%path)
    with open(str(path), 'r') as yaml_file:
        out = yaml.safe_load(yaml_file)
    return out
    
class FeatureHashComponent(UserDict):
    def __setitem__(self, key: Any, item: Any) -> None:
        if key not in self.data: self.data[key] = []
        return super().__setitem__(key, item)

    def __getitem__(self, key: Any) -> List[Any]:
        if key not in self.data: self.data[key] = []
        return self.data[key]

class FeatureHash(UserDict):
    def __setitem__(self, key: Any, item: Dict[str, Any]) -> None:
        assert isinstance(item, dict), "FeatureHash can be only populated by dicts"
        if key not in self.data: self.data[key] = FeatureHashComponent(**item)

    def __getitem__(self, key: Any) -> FeatureHashComponent:
        if key not in self.data: self.data[key] = FeatureHashComponent()
        return self.data[key]
    
    def to_dict(self):
        """filters out empty keys"""
        out_dict = {}
        for k, v in self.data.items():
            if len(v) == 0:
                continue
            out_dict[k] = dict(v)
        return out_dict

    def __iter__(self):
        iter_dict = self.to_dict()
        return iter(iter_dict)

class KeyIterator():
    def __init__(self, start=0, n=9):
        self._start = start
        self._n = n
        self.current_id = None
    def __iter__(self):
        self.current_id = self._start
        return self
    def __next__(self):
        key = f"{self.current_id:0{self._n}d}"
        self.current_id += 1
        return key
    @property
    def current_idx(self):
        return int(self.current_id)
    def from_int(self, x: int):
        key = f"{x:0{self._n}d}"
        return key.encode('utf-8')
    @staticmethod
    def from_str(x: str): 
        return x.encode('utf-8')
    @staticmethod
    def to_int(x: int):
        return int(x.decode('utf-8'))
    @staticmethod
    def to_str(x: str):
        return x.decode('utf-8')


class StatusBytes():
    def __init__(self): 
        self._bytearray = bytearray(1024)
        self._current_idx = 0

    def push(self, value: bool):
        self._bytearray[self._current_idx] = bool(value)
        self._current_idx += 1
        if self._current_idx == len(self._bytearray) - 1:
            self._bytearray += bytearray(1024)
        
    def close(self):
        self._bytearray = self._bytearray[:self._current_idx]
    
    def count(self): 
        return sum(self._bytearray)

    def nonzero(self): 
        # numpy is more efficient for large buffer (C-based)
        arr = np.frombuffer(self._bytearray, dtype=np.uint8)
        positions = set(np.flatnonzero(arr).tolist())
        return positions

    def __getstate__(self):
        return {'bytearray': self._bytearray}

    def __setstate__(self, state):
        self.__dict__.update(_bytearray=state['bytearray'] + bytearray(1024), _current_idx=len(state['bytearray']))

@contextlib.contextmanager 
def status_bytes():
    b = StatusBytes()
    try: 
        yield b
    finally:
        b.close()
        
        


