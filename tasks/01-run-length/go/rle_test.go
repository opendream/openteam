package rle

import "testing"

var cases = []struct{ in, want string }{
	{"", ""},
	{"XYZ", "X1Y1Z1"},
	{"AAAaaaBBB🦄🦄🦄🦄🦄CCCCCCCCCCCC", "A3a3B3🦄5C12"},
	{"HAAAAPPY🦄", "H1A4P2Y1🦄1"},
}

func TestEncode(t *testing.T) {
	for _, c := range cases {
		if got := Encode(c.in); got != c.want {
			t.Fatalf("Encode(%q) => %q, want %q", c.in, got, c.want)
		}
	}
}
