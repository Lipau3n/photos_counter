import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FileType:
    name: str
    extensions: List[str]


FILE_TYPES: List[FileType] = [
    FileType(name='JPEG', extensions=['jpg', 'jpeg']),
    FileType(name='RAW', extensions=[
        'raw',
        'dng',
        'arw', 'srf', 'sr2',  # Sony
        'rwl',  # Leica
        'raf',  # Fujifilm
        'nef', 'nrw',  # Nikon
        'crw', 'cr2', 'cr3',  # Canon
        'erf',  # Epson
        '3fr',  # Hasselblad
        'mef',  # Mamiya
        'mrw',  # Konica Minolta
        'orf',  # Olympus
        'ptx', 'pef',  # Pentax
        'rw2',  # Panasonic
        'srw',  # Samsung
        'x3f',  # Sigma
    ]),
]


class Counter:
    def __init__(self, path: str) -> None:
        self.path = path
        self.extensions = self._set_extensions()
        self.result: Dict[str, Dict[str, int]] = {}
        self.count()

    @staticmethod
    def _set_extensions() -> Dict[str, str]:
        extensions = {}
        for file_type in FILE_TYPES:
            for ext in file_type.extensions:
                extensions[ext] = file_type.name
        return extensions

    def _files_count(self, filenames: List[str]) -> Dict[str, int]:
        result_for_dir = defaultdict(int)
        filenames = map(lambda x: x.lower(), filenames)
        extensions = self.extensions.keys()
        for filename in filenames:
            try:
                file_ext = os.path.splitext(filename)[1].replace('.', '')
                if file_ext in extensions:
                    result_for_dir[self.extensions.get(file_ext)] += 1
            except:  # NOQA
                continue
        return dict(result_for_dir) or None

    def count(self):
        for i, item in enumerate(os.walk(self.path, topdown=True)):
            if i == 0:
                continue
            dir_path, _, filenames = item
            print_path = dir_path.replace(self.path, '')
            if result_for_dir := self._files_count(filenames):
                self.result[print_path] = result_for_dir

    def print_result(self):
        total_photos: int = 0
        total_by_ext: Dict[str, int] = defaultdict(int)
        for path, result in self.result.items():
            result_str = "\n".join(f"\t— {ext}: {count}" for ext, count in result.items())
            for ext, count in result.items():
                total_photos += count
                total_by_ext[ext] += count
            print(f"{path}:\n{result_str}")
        print("=" * 50)
        print(f"Total: {total_photos}")
        print("\n".join(f"\t— {ext}: {count}" for ext, count in total_by_ext.items()))


if __name__ == '__main__':
    try:
        path = sys.argv[1]
        if not os.path.exists(path):
            raise Exception
        counter = Counter(path)
        counter.print_result()
    except:  # NOQA
        exit("Invalid directory path to photos count")
