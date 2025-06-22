package counter

import (
	"sync/atomic"
)

var current int64

func NextID() int64 {
	return atomic.AddInt64(&current, 1) - 1
}
