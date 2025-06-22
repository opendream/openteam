package rle

// Encode returns the run‑length encoding of UTF‑8 string s.
//
// "AAB" → "A2B1"
import (
	"strconv"
	"strings"
)

func Encode(s string) string {
	if len(s) == 0 {
		return ""
	}

	var b strings.Builder
	runes := []rune(s)
	n := len(runes)
	count := 1

	for i := 1; i < n; i++ {
		if runes[i] == runes[i-1] {
			count++
		} else {
			b.WriteRune(runes[i-1])
			b.WriteString(strconv.Itoa(count))
			count = 1
		}
	}
	// Append the last group
	b.WriteRune(runes[n-1])
	b.WriteString(strconv.Itoa(count))

	return b.String()
}
