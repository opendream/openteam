package counter

import (
	"sync"
)

var (
	current int64
	mu      sync.Mutex
)

func NextID() int64 {
	mu.Lock()
	defer mu.Unlock()
	id := current
	current++
	return id
}
