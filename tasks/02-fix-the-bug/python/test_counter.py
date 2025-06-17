# test_counter.py
import concurrent.futures, buggy_counter as bc

def test_no_duplicates():
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as ex:
        ids = list(ex.map(lambda _: bc.next_id(), range(10_000)))
    assert len(ids) == len(set(ids)), "Duplicate IDs found!"
    print("✅ Test passed! No duplicate IDs.")

if __name__ == "__main__":
    test_no_duplicates()

