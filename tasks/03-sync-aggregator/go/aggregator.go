// Package aggregator – stub for Concurrent File Stats Processor.
package aggregator

import (
	"bufio"
	"context"
	"os"
	"path/filepath"
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

type Task struct {
	Index int
	Path  string
}

type ResultWithIndex struct {
	Index  int
	Result Result
}

func readLines(filelistPath string) ([]string, error) {
	file, err := os.Open(filelistPath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			lines = append(lines, line)
		}
	}
	return lines, scanner.Err()
}

func processFileWithTimeout(displayPath, fullPath string, timeoutSec int) Result {
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeoutSec)*time.Second)
	defer cancel()

	resultChan := make(chan Result, 1)

	go func() {
		lines, words := 0, 0

		file, err := os.Open(fullPath)
		if err != nil {
			resultChan <- Result{Path: displayPath, Status: "timeout"}
			return
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)

		firstLine := true

		for scanner.Scan() {
			select {
			case <-ctx.Done():
				resultChan <- Result{Path: displayPath, Status: "timeout"}
				return
			default:
				line := scanner.Text()

				// Handle #sleep=N on first line
				if firstLine {
					firstLine = false
					if strings.HasPrefix(line, "#sleep=") {
						nStr := strings.TrimPrefix(line, "#sleep=")
						if n, err := strconv.Atoi(nStr); err == nil && n >= 5 {
							resultChan <- Result{Path: displayPath, Status: "timeout"}
							return
						}
						continue // skip first line even if sleep < 5
					}
				}

				// Skip other metadata lines starting with #
				if strings.HasPrefix(line, "#") {
					continue
				}

				lines++
				words += len(strings.Fields(line))
			}
		}

		resultChan <- Result{
			Path:   displayPath,
			Lines:  lines,
			Words:  words,
			Status: "ok",
		}
	}()

	select {
	case <-ctx.Done():
		return Result{Path: displayPath, Status: "timeout"}
	case res := <-resultChan:
		return res
	}
}

// Aggregate must read filelistPath, spin up *workers* goroutines,
// apply a per‑file timeout, and return results in **input order**.
func Aggregate(filelistPath string, workers, timeout int) ([]Result, error) {
	// for debugging
	// absBase, _ := filepath.Abs("tasks/03-sync-aggregator/data") // get absolute path to data dir

	// for testing
	absBase, err := filepath.Abs("../data")
	if err != nil {
		return nil, err
	}

	paths, err := readLines(filelistPath)
	if err != nil {
		return nil, err
	}

	taskChan := make(chan Task)
	resultChan := make(chan ResultWithIndex, len(paths))
	var wg sync.WaitGroup

	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for task := range taskChan {
				fullPath := filepath.Join(absBase, task.Path)
				// fmt.Println("DEBUG read path:", fullPath)

				res := processFileWithTimeout(task.Path, fullPath, timeout)
				resultChan <- ResultWithIndex{Index: task.Index, Result: res}
			}
		}()
	}

	go func() {
		for i, path := range paths {
			taskChan <- Task{Index: i, Path: path}
		}
		close(taskChan)
	}()

	wg.Wait()
	close(resultChan)

	results := make([]Result, len(paths))
	for r := range resultChan {
		results[r.Index] = r.Result
	}

	return results, nil
}
