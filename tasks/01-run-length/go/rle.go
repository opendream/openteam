package rle

import (
	"strconv"
	"strings"
)

// Encode returns the run‑length encoding of UTF‑8 string s.
//
// "AAB" → "A2B1"
func Encode(s string) string {
	if len(s) == 0 {
		return ""
	}

	var sb strings.Builder
	count := 1
	prev := rune(s[0])
	for _, curr := range s[1:] {
		if curr == prev {
			count++
		} else {
			sb.WriteRune(prev)
			sb.WriteString(strconv.Itoa(count))
			prev = curr
			count = 1
		}
	}

	sb.WriteRune(prev)
	sb.WriteString(strconv.Itoa(count))

	return sb.String()
}
