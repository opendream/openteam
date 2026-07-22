from __future__ import annotations

import concurrent.futures
from pathlib import Path
import time


def _process_single_file(file_path: str, base_dir: Path, timeout: int) -> dict:
    full_path = base_dir / file_path

    content = full_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Rule 2: เช็ก #sleep=N
    if lines and lines[0].startswith("#sleep="):
        try:
            sleep_time = float(lines[0].split("=")[1].strip())
        except (IndexError, ValueError):
            sleep_time = 0.0

        # ตัดบรรทัด marker ออก
        lines = lines[1:]

        # สลีปแบบซอยย่อยเพื่อไม่ให้ Thread โดน Block และหลุดจังหวะได้ทันทีที่เกิน timeout
        start_time = time.perf_counter()
        
        # ถ้าระบบตั้งใจให้สลีปนาน เช่น 5 หรือ 10 วิ แต่ timeout แค่ 2 วิ
        # จะวนลูปสลีปแค่ถึง timeout แล้วยกเลิกทันที ไม่รอนอนจนครบ 10 วิ
        while time.perf_counter() - start_time < sleep_time:
            # ถ้าระหว่างนอน เวลาสะสมเกิน timeout แล้ว ให้โยน TimeoutError ออกไปทันที
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError()
            
            # สลีปทีละช่วงเวลาสั้นๆ (เช่น 0.02 วินาที)
            time.sleep(min(0.02, sleep_time - (time.perf_counter() - start_time)))

    # Rule 3: นับ Lines และ Words
    line_count = len(lines)
    text_remaining = "\n".join(lines)
    word_count = len(text_remaining.split())

    return {
        "path": file_path,
        "lines": line_count,
        "words": word_count,
        "status": "ok",
    }


def aggregate(filelist_path: str, workers: int = 4, timeout: int = 2) -> list[dict]:
    filelist_file = Path(filelist_path)
    base_dir = filelist_file.parent

    paths = [
        line.strip()
        for line in filelist_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(_process_single_file, path, base_dir, timeout)
            for path in paths
        ]

        for path, future in zip(paths, futures):
            try:
                result = future.result()
            except (concurrent.futures.TimeoutError, TimeoutError):
                result = {"path": path, "status": "timeout"}

            results.append(result)

    return results