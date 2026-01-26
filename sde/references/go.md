# Go Coding Guidelines

This document outlines the latest coding standards and best practices for Go. Please refer to this document when developing Go projects.

## 1. Official Tooling
- **gofmt**: Must use `gofmt` (or `goimports`) for code formatting.
  - Follow the standard Go style (tabs for indentation).
- **go vet**: Use `go vet` to identify common mistakes that the compiler does not catch.
- **golangci-lint**: Strongly recommended for comprehensive linting.
  - Address warnings during development.
  - Configure critical linters like `errcheck`, `staticcheck`, and `unused`.

## 2. Naming Conventions
- **MixedCaps**: Use `MixedCaps` or `mixedCaps` rather than underscores (`snake_case`) for multi-word names.
- **Exported Names**: Names starting with an upper-case letter are exported (public); others are unexported (package-private).
- **Acronyms**: Keep acronyms in consistent case (e.g., `ServeHTTP`, `URLRouter`, not `ServeHttp` or `UrlRouter`).
- **Variables**: Short variable names are preferred for short scopes (e.g., `i` for index, `r` for reader).
- **Packages**: Use short, lowercase, single-word names for packages.

## 3. Idiomatic Go
- **Error Handling**:
  - Functions that can fail should return an `error` as the last return value.
  - Always check for errors immediately: `if err != nil { return err }`.
  - Use `fmt.Errorf` with the `%w` verb to wrap errors for context.
- **Receiver Consistency**: Use pointer receivers (`*T`) consistently if any method requires one, or to avoid copying large structs.
- **Interfaces**:
  - Keep interfaces small (e.g., `io.Reader`, `io.Writer`).
  - Define interfaces where they are used (consumer side) rather than where the implementation is defined.
- **Defer**: Use `defer` to ensure resources (files, locks, network connections) are released promptly.

## 4. Concurrency
- **Goroutines**: Lightweight threads. Do not leak goroutines; ensure they have a clear exit path.
- **Channels**: Use channels to communicate between goroutines. Avoid shared state where possible.
- **sync Package**: Use `sync.Mutex` or `sync.RWMutex` when low-level synchronization is necessary.
- **Context**: Use `context.Context` to manage timeouts, deadlines, and cancellation signals across API boundaries and goroutines.

## 5. Unit Test Best Practices
- **Testing Package**: Use the standard `testing` package.
- **Table-Driven Tests**: Preferred for testing multiple scenarios with the same logic.
  ```go
  func TestSum(t *testing.T) {
      tests := []struct {
          name     string
          input    []int
          expected int
      }{
          {"empty", []int{}, 0},
          {"positive", []int{1, 2}, 3},
      }
      for _, tt := range tests {
          t.Run(tt.name, func(t *testing.T) {
              if got := Sum(tt.input); got != tt.expected {
                  t.Errorf("Sum() = %v, want %v", got, tt.expected)
              }
          })
      }
  }
  ```
- **Naming**: Test functions must start with `Test` followed by the function name (e.g., `TestCalculate`).
- **Assertions**: Use [github.com/stretchr/testify/assert](https://github.com/stretchr/testify) or `github.com/stretchr/testify/require` for all assertions.
  - Use `assert` for non-fatal failures (test continues).
  - Use `require` for fatal failures (test stops immediately).
  ```go
  import (
      "testing"
      "github.com/stretchr/testify/assert"
  )

  func TestSum(t *testing.T) {
      got := Sum(1, 2)
      assert.Equal(t, 3, got, "they should be equal")
  }
  ```
- **Mocking**: Use interfaces to mock external dependencies. Strongly recommend using `github.com/stretchr/testify/mock`. Tools like `mockery` can generate these mocks automatically.
- **Test Coverage**:
  - Use `go test -cover` to check coverage.
  - **Requirement**: Overall Unit Test coverage must be **85% or higher**.
- **Edge Cases**: Always test nil pointers, empty slices, zero values, and error conditions.
