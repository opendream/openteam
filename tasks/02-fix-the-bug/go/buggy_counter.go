package counter

import (
	"sync/atomic"
	"time"
)

var current int64

func NextID() int64 {
	// use atomic to add a current to avoid a race
	id := atomic.AddInt64(&current, 1) - 1
	time.Sleep(0)
	return id
}
