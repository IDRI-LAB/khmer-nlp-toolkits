import os
import tqdm
import subprocess
import jsonlines


def get_filepath(source: str, destination: str = None):
    filenames = sorted([entry.name for entry in os.scandir(source) if entry.is_file()])
    if destination:
        os.makedirs(destination, exist_ok=True)
        return [(os.path.join(source, name), os.path.join(destination, name)) for name in filenames]
    return [os.path.join(source, name) for name in filenames]


def count_file_line(filepath: str):
    lines = subprocess.run(["wc", "-l", filepath], capture_output=True)
    lines = int(lines.stdout.decode("utf-8").split(" ")[0])
    return lines


def lazy_read_jsonl(filepath, allow_none=True, limit: int = None, show_progress: bool = False):
    class LazyReadJsonl:
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
