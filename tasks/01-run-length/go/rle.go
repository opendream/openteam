package rle

import "fmt"

// Encode returns the run‑length encoding of UTF‑8 string s.
//
// "AAB" → "A2B1"
func Encode(s string) string {
	if len(s) == 0 {
		return ""
	}
	result := ""
	count := 1
	sr := []rune(s)
	for i := 1; i < len(sr); i++ {
		if sr[i] == sr[i-1] {
			count++
			continue
		}
		result += fmt.Sprintf("%c%d", sr[i-1], count)
		count = 1
	}
	result += fmt.Sprintf("%c%d", sr[len(sr)-1], count)
	return result
}
