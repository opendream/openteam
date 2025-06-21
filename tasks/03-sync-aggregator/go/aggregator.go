// Package aggregator – stub for Concurrent File Stats Processor.
package aggregator

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"strconv"
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
// Job represents a file processing task with its original order
type Job struct {
	Path  string
	Index int // Original position in the file list
}

// JobResult contains the result with its original index for ordering
type JobResult struct {
	Result Result
	Index  int
}

// Aggregate must read filelistPath, spin up *workers* goroutines,
// apply a per‑file timeout, and return results in **input order**.
func Aggregate(filelistPath string, workers, timeout int) ([]Result, error) {
	// ── TODO: IMPLEMENT ────────────────────────────────────────────────────────
	// iterate over the file list
	filePaths, err := readFileList(filelistPath)
	if err != nil {
		return nil, fmt.Errorf("failed to read file list: %w", err)
	}

	if len(filePaths) == 0 {
		return []Result{}, nil
	}

	// create channels for job distribution
	jobs := make(chan Job, len(filePaths))
	results := make(chan JobResult, len(filePaths))

	// Start worker goroutines
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go worker(jobs, results, time.Duration(timeout)*time.Second, &wg)
	}

	// Send jobs to workers
	go func() {
		defer close(jobs)
		for i, path := range filePaths {
			jobs <- Job{Path: path, Index: i}
		}
	}()

	// Collect results
	go func() {
		wg.Wait()
		close(results)
	}()
	// Gather all results
	jobResults := make([]JobResult, 0, len(filePaths))
	for result := range results {
		jobResults = append(jobResults, result)
	}

	// Sort results by original index to maintain input order
	orderedResults := make([]Result, len(filePaths))
	for _, jr := range jobResults {
		orderedResults[jr.Index] = jr.Result
	}
	return orderedResults, nil
	// ───────────────────────────────────────────────────────────────────────────
}
// readFileList reads the file list from the given path
func readFileList(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var paths []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			paths = append(paths, line)
		}
	}

	return paths, scanner.Err()
}

// worker processes jobs with timeout
func worker(jobs <-chan Job, results chan<- JobResult, timeout time.Duration, wg *sync.WaitGroup) {
	defer wg.Done()

	for job := range jobs {
		result := processFileWithTimeout(job.Path, timeout)
		results <- JobResult{
			Result: result,
			Index:  job.Index,
		}
	}
}

// processFileWithTimeout processes a single file with timeout
func processFileWithTimeout(filePath string, timeout time.Duration) Result {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	// Channel to receive the processing result
	resultChan := make(chan Result, 1)

	// Process file in a separate goroutine
	go func() {
		result := processFile(filePath)
		select {
		case resultChan <- result:
		case <-ctx.Done():
			// Context cancelled, don't send result
		}
	}()

	// Wait for either completion or timeout
	select {
	case result := <-resultChan:
		return result
	case <-ctx.Done():
		return Result{
			Path:   filePath,
			Lines:  0,
			Words:  0,
			Status: "timeout",
		}
	}
}

// processFile processes a single file and counts lines/words
func processFile(filePath string) Result {
	file, err := os.Open(filePath)
	if err != nil {
		return Result{
			Path:   filePath,
			Lines:  0,
			Words:  0,
			Status: "error",
		}
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	lines := 0
	words := 0
	firstLine := true

	for scanner.Scan() {
		line := scanner.Text()

		// Handle sleep marker on first line
		if firstLine {
			firstLine = false
			if strings.HasPrefix(line, "#sleep=") {
				// Extract sleep duration and sleep
				sleepStr := strings.TrimPrefix(line, "#sleep=")
				if sleepDuration, err := strconv.Atoi(sleepStr); err == nil {
					time.Sleep(time.Duration(sleepDuration) * time.Second)
				}
				continue // Skip this line from counting
			}
		}

		// Count this line
		lines++

		// Count words (ASCII whitespace-separated tokens)
		fields := strings.Fields(line)
		words += len(fields)
	}

	if err := scanner.Err(); err != nil {
		return Result{
			Path:   filePath,
			Lines:  0,
			Words:  0,
			Status: "error",
		}
	}

	return Result{
		Path:   filePath,
		Lines:  lines,
		Words:  words,
		Status: "ok",
	}
}
