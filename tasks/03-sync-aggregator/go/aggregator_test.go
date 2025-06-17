package aggregator

import (
	"path/filepath"
	"testing"
	"time"
)

var _expected = []Result{
	{"texts/01_lorem.txt", 5, 69, "ok"},
	{"texts/02_zen.txt", 8, 39, "ok"},
	{"texts/03_bacon.txt", 3, 38, "ok"},
	{"texts/04_proverbs.txt", 5, 25, "ok"},
	{"texts/05_poem.txt", 5, 37, "ok"},
	{"texts/06_quote.txt", 2, 12, "ok"},
	{"texts/07_sleep5.txt", 0, 0, "timeout"},
	{"texts/08_sleep10.txt", 0, 0, "timeout"},
	{"texts/09_scifi.txt", 4, 47, "ok"},
	{"texts/10_short.txt", 1, 2, "ok"},
	{"texts/11_manifesto.txt", 4, 49, "ok"},
	{"texts/12_jokes.txt", 3, 45, "ok"},
	{"texts/13_ai_ghosts.txt", 6, 83, "ok"},
	{"texts/14_funfacts.txt", 3, 52, "ok"},
	{"texts/15_trivia.txt", 3, 58, "ok"},
}

func TestAggregateMatchesExpected(t *testing.T) {
	filelist := filepath.Join("..", "data", "filelist.txt")

	start := time.Now()
	results, err := Aggregate(filelist, 8, 2)
	if err != nil {
		t.Fatalf("aggregate failed: %v", err)
	}
	elapsed := time.Since(start)

	if len(results) != len(_expected) {
		t.Fatalf("got %d records, want %d", len(results), len(_expected))
	}

	for i, got := range results {
		want := _expected[i]
		if got.Path != want.Path || got.Status != want.Status {
			t.Errorf("record %d mismatch: got %+v, want %+v", i, got, want)
			continue
		}
		if got.Status == "ok" && (got.Lines != want.Lines || got.Words != want.Words) {
			t.Errorf("%s lines/words mismatch: got %+v, want %+v", got.Path, got, want)
		}
	}

	if elapsed > 6*time.Second {
		t.Errorf("processing too slow (%v); expected concurrency", elapsed)
	}
}
