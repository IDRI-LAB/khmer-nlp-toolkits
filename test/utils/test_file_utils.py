import pytest
import os
import tempfile
import subprocess
import jsonlines

from khmer_nlp_toolkits.utils.file_utils import get_filepath, count_file_line, lazy_read_jsonl


def test_returns_sorted_file_paths_without_destination():
    with tempfile.TemporaryDirectory() as source:
        open(os.path.join(source, "b.txt"), "w").close()
        open(os.path.join(source, "a.txt"), "w").close()

        # directory should be ignored
        os.mkdir(os.path.join(source, "folder"))

        result = get_filepath(source)

        expected = [
            os.path.join(source, "a.txt"),
            os.path.join(source, "b.txt"),
        ]

        assert result == expected


def test_returns_source_destination_pairs_with_destination():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as base_dest:
        destination = os.path.join(base_dest, "output")

        open(os.path.join(source, "b.txt"), "w").close()
        open(os.path.join(source, "a.txt"), "w").close()

        result = get_filepath(source, destination)

        expected = [
            (
                os.path.join(source, "a.txt"),
                os.path.join(destination, "a.txt"),
            ),
            (
                os.path.join(source, "b.txt"),
                os.path.join(destination, "b.txt"),
            ),
        ]

        assert result == expected
        assert os.path.isdir(destination)


def test_empty_source_directory():
    with tempfile.TemporaryDirectory() as source:
        result = get_filepath(source)

        assert result == []


def test_empty_source_directory_with_destination():
    with tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as base_dest:
        destination = os.path.join(base_dest, "output")

        result = get_filepath(source, destination)

        assert result == []
        assert os.path.isdir(destination)


# from your_module import count_file_line

def test_count_file_line(tmp_path):
    file = tmp_path / "sample.txt"

    file.write_text(
        "line1\n"
        "line2\n"
        "line3\n"
    )

    result = count_file_line(str(file))

    assert result == 3


def test_count_empty_file(tmp_path):
    file = tmp_path / "empty.txt"

    file.write_text("")

    result = count_file_line(str(file))

    assert result == 0


def test_count_single_line_file(tmp_path):
    file = tmp_path / "single.txt"

    file.write_text("hello\n")

    result = count_file_line(str(file))

    assert result == 1


def test_nonexistent_file_raises_error():
    with pytest.raises(subprocess.CalledProcessError):
        count_file_line("does_not_exist.txt")


# from your_module import lazy_read_jsonl

def test_lazy_read_jsonl_reads_all_lines(tmp_path):
    file = tmp_path / "data.jsonl"

    records = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]

    with jsonlines.open(file, "w") as writer:
        writer.write_all(records)

    reader = lazy_read_jsonl(str(file))

    assert len(reader) == 3
    assert list(reader) == records


def test_lazy_read_jsonl_with_limit(tmp_path):
    file = tmp_path / "data.jsonl"

    records = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]

    with jsonlines.open(file, "w") as writer:
        writer.write_all(records)

    reader = lazy_read_jsonl(str(file), limit=2)

    assert len(reader) == 2
    assert list(reader) == [
        {"id": 1},
        {"id": 2},
    ]


def test_lazy_read_jsonl_empty_file(tmp_path):
    file = tmp_path / "empty.jsonl"
    file.write_text("")

    reader = lazy_read_jsonl(str(file))

    assert len(reader) == 0
    assert list(reader) == []


def test_lazy_read_jsonl_allow_none_true(tmp_path):
    file = tmp_path / "data.jsonl"

    with jsonlines.open(file, "w") as writer:
        writer.write({"id": 1})
        writer.write(None)
        writer.write({"id": 2})

    reader = lazy_read_jsonl(str(file), allow_none=True)

    assert len(reader) == 3
    assert list(reader) == [
        {"id": 1},
        None,
        {"id": 2},
    ]


def test_lazy_read_jsonl_is_lazy_iterator(tmp_path):
    file = tmp_path / "data.jsonl"

    records = [
        {"id": 1},
        {"id": 2},
    ]

    with jsonlines.open(file, "w") as writer:
        writer.write_all(records)

    reader = lazy_read_jsonl(str(file))

    assert iter(reader) is reader
    assert next(reader) == {"id": 1}
    assert next(reader) == {"id": 2}

    with pytest.raises(StopIteration):
        next(reader)
