package counter

import (
	"sync"
	"time"
)

var current int64
var mu sync.Mutex

func NextID() int64 {
	// 	it's a race condition problem with goroutine where we face a problem with read, write, modify value by allowing a goroutine do a task that run as a background and make it unsyncronized
	//  then it can make goroutine accessing current value simultaneously not in an order
	// 	it can lead to lost an update of value and return the same ID
	// 	so we need to make it as atomic operation
	// 	using Mutex to make it as a syncronize before we do an operation
	mu.Lock() // lock a code and allow only one goroutine at a time to make it syncronized
	defer mu.Unlock()

	id := current 
	time.Sleep(0)
	current++
	return id
}
