"""
Utility module.
"""
import os
import subprocess

import tqdm
import jsonlines


def get_filepath(source: str, destination: str = None):
    """
    Retrieves and sorts file paths from a source directory, optionally mapping them to a destination.

    If a destination is provided, it ensures the directory exists and returns a list
    of tuples containing (source_path, destination_path). Otherwise, it returns
    a list of full paths to the files in the source directory.

    Args:
        source: str
            The directory path to scan for files.
        destination: str, optional
            The directory path where files are intended to be mapped or moved. Defaults to None.

    Returns:
        list:
            A list of strings (source paths) if destination is None.
        list[tuple]:
            A list of (source_path, destination_path) pairs if destination is provided.
    """
    filenames = sorted([entry.name for entry in os.scandir(source) if entry.is_file()])
    if destination:
        os.makedirs(destination, exist_ok=True)
        return [(os.path.join(source, name), os.path.join(destination, name)) for name in filenames]
    return [os.path.join(source, name) for name in filenames]


def count_file_line(filepath: str) -> int:
    """
    Count line in file using subprocess. Better for big file.
    """
    lines = subprocess.run(["wc", "-l", filepath], capture_output=True, text=True, check=True)
    lines = int(lines.stdout.split(" ")[0])
    return lines


def lazy_read_jsonl(filepath, allow_none=True, limit: int = None, show_progress: bool = False):
    """
    Lazy read json from jsonline file. Consume data line-by-line with generator when called.
    """
    class LazyReadJsonl:
        """
        Wrapper class for generator cosume and metadata provider.
        """
        def __init__(self, filepath):
            self.index = -1
            self.length = count_file_line(filepath)
            if limit is not None and self.length > limit:
                self.length = limit

            def data_generator():
                with jsonlines.open(filepath, "r") as reader:
                    iterator = reader.iter(allow_none=allow_none)
                    if show_progress:
                        iterator = tqdm.tqdm(iterator, total=self.length, desc="Reading", mininterval=0.2)
                    for data in iterator:
                        if self.index == limit:
                            break
                        yield data
            self.generator = data_generator()

        def __iter__(self):
            return self

        def __next__(self):
            self.index += 1
            return next(self.generator)

        def __len__(self):
            return self.length
    return LazyReadJsonl(filepath)
