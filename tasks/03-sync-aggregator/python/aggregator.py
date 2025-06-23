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
import time
import os
import re


def process_file(filepath: str, timeout: int) -> Dict:
    """
    Process a single file with timeout enforcement.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        sleep_time = 0
        content_lines = lines
        
        if lines and lines[0].strip().startswith('#sleep='):
            sleep_match = re.match(r'#sleep=(\d+)', lines[0].strip())
            if sleep_match:
                sleep_time = int(sleep_match.group(1))
                content_lines = lines[1:]
                
                if sleep_time > timeout:
                    raise TimeoutError("Sleep duration exceeds timeout")
        
        if sleep_time > 0:
            time.sleep(sleep_time)
        
        line_count = len(content_lines)
        word_count = 0
        
        for line in content_lines:
            words = line.split()
            word_count += len(words)
        
        return {
            "path": filepath,
            "lines": line_count,
            "words": word_count,
            "status": "ok"
        }
        
    except Exception as e:
        return {
            "path": filepath,
            "status": "timeout"
        }



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
    try:
        with open(filelist_path, 'r', encoding='utf-8') as f:
            file_paths = [line.strip() for line in f if line.strip()]
    except Exception:
        return []
    
    if not file_paths:
        return []
    
    base_dir = os.path.dirname(filelist_path)
    
    results = [None] * len(file_paths)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_index = {}
        for i, filepath in enumerate(file_paths):
            full_path = os.path.join(base_dir, filepath) if not os.path.isabs(filepath) else filepath
            future = executor.submit(process_file, full_path, timeout)
            future_to_index[future] = i
        
        for future in future_to_index.keys():
            index = future_to_index[future]
            original_filepath = file_paths[index]
            
            try:
                result = future.result(timeout=timeout)
                result["path"] = original_filepath
                results[index] = result
            except concurrent.futures.TimeoutError:
                results[index] = {
                    "path": original_filepath,
                    "status": "timeout"
                }
            except Exception:
                results[index] = {
                    "path": original_filepath,
                    "status": "timeout"
                }
    
    return results
