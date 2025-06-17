package main

import (
	"fmt"
	"sync"
	// "sync/atomic"
)

// var current int64
var (
	current int64
	mu      sync.Mutex
)

func NextID() int64 {
	// atomic.AddInt64(&current, 1) // Increment current atomically
	mu.Lock()
	defer mu.Unlock()
	id := current
	current++
	return id
}

func main() {
	var wg sync.WaitGroup

	for i := 0; i < 5000; i++ {
		wg.Add(1)
		go func() {
			fmt.Println(NextID())
			wg.Done()
		}()
	}

	wg.Wait()
}
