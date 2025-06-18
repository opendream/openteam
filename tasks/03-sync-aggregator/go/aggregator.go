// Package aggregator – stub for Concurrent File Stats Processor.
package aggregator

import (
	"bufio"
	"context"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// Result mirrors one JSON object in the final array.
type Result struct {
	Path   string `json:"path"`
	Lines  int    `json:"lines,omitempty"`
	Words  int    `json:"words,omitempty"`
	Status string `json:"status"` // "ok" or "timeout"
}

// Aggregate must read filelistPath, spin up *workers* goroutines,
// apply a per‑file timeout, and return results in **input order**.
func Aggregate(filelistPath string, workers, timeout int) ([]Result, error) {
	// ── TODO: IMPLEMENT ────────────────────────────────────────────────────────
	file, err := os.Open(filelistPath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var paths []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		paths = append(paths, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	fileIndex := make(map[string]int)
	for i, path := range paths {
		fileIndex[path] = i
	}

	jobs := make(chan string)
	results := make(chan Result)
	output := make([]Result, len(paths))
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeout)*time.Second)
	defer cancel()

	worker(ctx, workers, jobs, results)
	job(ctx, paths, jobs)

	for {
		select {
		case res, ok := <-results:
			if !ok {
				return output, nil
			}
			index, _ := fileIndex[res.Path]
			output[index] = res
		}
	}
	// ───────────────────────────────────────────────────────────────────────────
}

func job(ctx context.Context, paths []string, jobs chan<- string) {
	go func() {
		defer close(jobs)
		for _, path := range paths {
			select {
			case <-ctx.Done():
				return
			case jobs <- path:
			}
		}
	}()

}

func worker(ctx context.Context, workers int, jobs <-chan string, results chan<- Result) {
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for {
				select {
				case <-ctx.Done():
					return
				case path, ok := <-jobs:
					if !ok {
						return
					}
					lines, words, err := readFile(ctx, path)
					status := "ok"
					if err != nil {
						status = "timeout"
					}
					results <- Result{
						Path:   path,
						Lines:  lines,
						Words:  words,
						Status: status,
					}
				}
			}
		}()
	}
	go func() {
		wg.Wait()
		close(results)
	}()
}

func readFile(ctx context.Context, path string) (int, int, error) {
	filelist := filepath.Join("..", "data", path)
	f, _ := os.Open(filelist)
	defer f.Close()
	scanner := bufio.NewScanner(f)
	lineCount := 0
	wordCount := 0
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "#sleep=") {
			sleepDur := strings.TrimPrefix(line, "#sleep=")
			sleepSec, _ := time.ParseDuration(sleepDur + "s")
			select {
			case <-time.After(sleepSec):
			case <-ctx.Done():
				return lineCount, wordCount, ctx.Err()
			}
			continue
		}
		wordCount += len(strings.Fields(line))
		lineCount++
	}

	return lineCount, wordCount, scanner.Err()
}
