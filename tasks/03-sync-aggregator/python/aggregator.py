"""
Concurrent File Stats Processor – Python stub.

Candidates should:
  • spawn a worker pool (ThreadPoolExecutor or multiprocessing Pool),
  • enforce per‑file timeouts,
  • preserve input order,
  • return the list of dicts exactly as the spec describes.
"""
from __future__ import annotations
from typing import List, Dict
import concurrent.futures
import os, time

def _process_file(full_path: str, timeout: int) -> Dict:
    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if lines and lines[0].startswith("#sleep="):
        sleep_time = int(lines[0].split("=")[1])
        if sleep_time > timeout:
            return {"status": "timeout"}
        time.sleep(sleep_time)
        lines = lines[1:]

    word_count = sum(len(line.split()) for line in lines)
    return {"lines": len(lines), "words": word_count, "status": "ok"}


def aggregate(filelist_path: str, workers: int = 4, timeout: int = 2) -> List[Dict]:
    """
    Process every path listed in *filelist_path* concurrently.

    Returns a list of dictionaries in the *same order* as the incoming paths.

    Each dictionary must contain:
        {"path": str, "lines": int, "words": int, "status": "ok"}
    or, on timeout:
        {"path": str, "status": "timeout"}

    Parameters
    ----------
    filelist_path : str
        Path to text file containing one relative file path per line.
    workers : int
        Maximum number of concurrent worker threads.
    timeout : int
        Per‑file timeout budget in **seconds**.
    """
    base_dir = os.path.dirname(filelist_path)
    with open(filelist_path, "r", encoding="utf-8") as f:
        relative_paths = [line.strip() for line in f if line.strip()]
    
    results: List[Dict] = [{}] * len(relative_paths)
    # results = []
    # results: List[Dict] = [None] * len(relative_paths)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_process_file, os.path.join(base_dir, p), timeout): (i, p)
            for i, p in enumerate(relative_paths)
        }

        for future in concurrent.futures.as_completed(futures):
            i, rel_path = futures[future]
            try:
                result = future.result()
                result["path"] = rel_path
            except Exception as e:
                result = {"path": rel_path, "status": "error"}
            results[i] = result

    return results