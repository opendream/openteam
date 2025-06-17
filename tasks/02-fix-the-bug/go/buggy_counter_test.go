package counter

import (
	"sync"
	"testing"
)

func TestNextID_NoDuplicates(t *testing.T) {
	const N = 5_000

	var (
		ids = make([]int64, N)
		wg  sync.WaitGroup
	)
	wg.Add(N)

	for i := 0; i < N; i++ {
		go func(i int) {
			defer wg.Done()
			ids[i] = NextID()
		}(i)
	}
	wg.Wait()

	seen := make(map[int64]struct{}, N)
	for _, id := range ids {
		if _, dup := seen[id]; dup {
			t.Fatalf("duplicate id %d detected", id)
		}
		seen[id] = struct{}{}
	}
}
