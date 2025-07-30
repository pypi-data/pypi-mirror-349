import math
import psutil
from pydantic import PositiveInt
from pathlib import Path
from . import py

# todo: add automatic fallback to py functions if rust is unavailable
try:
    from . import rs
except ImportError:
    # todo: replace with custom exception
    raise Exception(
        "Missing rust binaries. Please submit a GitHub issue and I'll try and get to the bottom of this."
    )

# TODO: move
FilePath = str | Path
max_thread_use_perc = 0.8
available_threads = psutil.cpu_count(logical=True) or 1
usable_threads = math.ceil(max_thread_use_perc * available_threads)


def count_lines_in_file(
    path: FilePath,
    chunk: PositiveInt = 1 << 20,
    threads: PositiveInt | None = None,
) -> int:
    """
    Count the number of lines in a file.

    Args:
        path (FilePath): Path to the file.
        chunk_size (PositiveInt, optional): Size of chunks to read in bytes. Defaults to 1<<20.
        num_threads (PositiveInt | None, optional): Number of threads to use. If `None`, automatically determined.

    Returns:
        int: _description_
    """
    _path = Path(path)
    _threads = threads or usable_threads
    if not _path.exists():
        raise FileNotFoundError(path)
    if chunk < 1:
        raise ValueError(
            f"'chunk_size' must be a positive integer, is: {chunk}"
        )
    if _threads < 1:
        raise ValueError(
            f"'threads' must be a positive integer, is: {threads}"
        )
    elif _threads > usable_threads:
        raise ValueError(
            f"Requested threads exceeds allocated maximum ({threads} > {usable_threads})"
        )
    return rs.count_lines_in_file(str(path), chunk, _threads)
