import os
import subprocess
import jsonlines


def get_filepath(source: str, destination: str = None):
    filenames = sorted(os.listdir(source))
    if destination:
        os.makedirs(destination, exist_ok=True)
        return [(os.path.join(source, name), os.path.join(destination, name)) for name in filenames]
    return [os.path.join(source, name) for name in filenames]


def count_file_line(filepath: str):
    lines = subprocess.run(["wc", "-l", filepath], capture_output=True)
    lines = int(lines.stdout.decode("utf-8").split(" ")[0])
    return lines


def lazy_read_jsonl(filepath, allow_none=True):
    class LazyReadJsonl:
        def __init__(self, filepath):
            self.index = -1
            self.length = count_file_line(filepath)
            def data_generator():
                with jsonlines.open(filepath, "r") as reader:
                    for data in reader.iter(allow_none=allow_none):
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
