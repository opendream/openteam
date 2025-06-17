"""
Concurrent File Stats Processor – Python stub.

Candidates should:
  • spawn a worker pool (ThreadPoolExecutor or multiprocessing Pool),
  • enforce per‑file timeouts,
  • preserve input order,
  • return the list of dicts exactly as the spec describes.
"""

from __future__ import annotations
from typing import List, Dict, Tuple, Optional
import time
import pathlib
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


def _process_file(base_dir: str, rel_path: str) -> Dict:
    """Process a single file and return its statistics."""
    path = os.path.join(base_dir, rel_path)

    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()

        # Handle sleep directive if present
        if lines and lines[0].startswith("#sleep="):
            sleep_time = int(lines[0].strip().split("=")[1])
            if sleep_time > 0:
                time.sleep(sleep_time)
            lines = lines[1:]  # Remove sleep directive from counting

        line_count = len(lines)
        word_count = sum(len(line.split()) for line in lines)

        return {
            "path": rel_path,
            "lines": line_count,
            "words": word_count,
            "status": "ok",
        }
    except Exception:
        return {"path": rel_path, "status": "timeout"}


def _process_file_with_timeout(io_task: Tuple[str, str, int]) -> Dict:
    """Wrapper function to handle timeout for a single file."""
    base_dir, rel_path, timeout = io_task

    try:
        result: List[Optional[Dict]] = [None]
        exception: List[Optional[Exception]] = [None]

        def worker():
            try:
                result[0] = _process_file(base_dir, rel_path)
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            thread.join(0.2) # adding buffer time 200ms to handle the exact timeout boundary as thread finishes
            if thread.is_alive():
                # Thread exceeded timeout - abandon it
                return {"path": rel_path, "status": "timeout"}

        if exception[0]:
            return {"path": rel_path, "status": "timeout"}

        return result[0] if result[0] else {"path": rel_path, "status": "timeout"}

    except Exception:
        return {"path": rel_path, "status": "timeout"}


def aggregate(filelist_path: str, workers: int = 4, timeout: int = 2) -> List[Dict]:
    """
    Process files concurrently with worker pool and per-file timeouts.
    Returns results in the same order as the input filelist.
    """
    base_dir = str(pathlib.Path(filelist_path).parent)

    with open(filelist_path, encoding="utf-8") as f:
        relative_file_paths = [line.strip() for line in f if line]

    io_tasks_list = [(base_dir, rel_path, timeout) for rel_path in relative_file_paths]

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Map futures to original indices to preserve order
        future_to_index = {
            executor.submit(_process_file_with_timeout, io_task): i
            for i, io_task in enumerate(io_tasks_list)
        }

        results: List[Dict] = [{}] * len(relative_file_paths)

        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                result = future.result()
                results[index] = result
            except Exception:
                results[index] = {
                    "path": relative_file_paths[index],
                    "status": "timeout",
                }

    return results
