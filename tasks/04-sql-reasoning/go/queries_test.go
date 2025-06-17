// tasks/04‑sql‑reasoning/go/queries_test.go
package queries

import (
	"database/sql"
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"testing"

	_ "github.com/mattn/go-sqlite3"
)

func rootDir(t *testing.T) string {
	dir, err := filepath.Abs(filepath.Join(".."))
	if err != nil {
		t.Fatalf("abs path: %v", err)
	}
	return dir
}

func dbPath(t *testing.T) string { return filepath.Join(rootDir(t), "donations.db") }
func expPath(t *testing.T, name string) string {
	return filepath.Join(rootDir(t), "expected", name)
}

func fetch(t *testing.T, sqlStr string) ([]string, [][]string) {
	db, err := sql.Open("sqlite3", dbPath(t))
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	defer db.Close()

	rows, err := db.Query(sqlStr)
	if err != nil {
		t.Fatalf("query: %v", err)
	}
	defer rows.Close()

	cols, _ := rows.Columns()
	data := [][]string{}
	for rows.Next() {
		raw := make([]interface{}, len(cols))
		ptrs := make([]interface{}, len(cols))
		for i := range raw {
			ptrs[i] = &raw[i]
		}
		if err := rows.Scan(ptrs...); err != nil {
			t.Fatalf("scan: %v", err)
		}
		rec := make([]string, len(cols))
		for i, v := range raw {
			if v == nil {
				rec[i] = ""
			} else {
				rec[i] = fmt.Sprint(v)
			}
		}
		data = append(data, rec)
	}
	return cols, data
}

func loadExpected(t *testing.T, name string) ([]string, [][]string) {
	f, err := os.Open(expPath(t, name))
	if err != nil {
		t.Fatalf("open exp: %v", err)
	}
	defer f.Close()
	r := csv.NewReader(f)
	header, _ := r.Read()
	body, _ := r.ReadAll()
	return header, body
}

func TestTaskA(t *testing.T) {
	expH, expR := loadExpected(t, "q1.csv")
	gotH, gotR := fetch(t, SQLA)
	if !reflect.DeepEqual(expH, gotH) || !reflect.DeepEqual(expR, gotR) {
		t.Fatalf("Task A mismatch")
	}
}

func TestTaskB(t *testing.T) {
	expH, expR := loadExpected(t, "q2.csv")
	gotH, gotR := fetch(t, SQLB)
	if !reflect.DeepEqual(expH, gotH) || !reflect.DeepEqual(expR, gotR) {
		t.Fatalf("Task B mismatch")
	}
}
