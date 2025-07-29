# Memuri Tests

This directory contains tests for the Memuri system, including unit tests, integration tests, and performance benchmarks.

## Latency Tests

The latency tests are designed to measure the performance of memory operations in the Memuri system. These tests can be used to:

1. Establish performance baselines
2. Detect performance regressions
3. Optimize memory operations
4. Validate performance on different hardware or configurations

### Running Latency Tests

You can run the latency tests using the provided command-line script:

```bash
# Run all latency tests with default settings
./run_latency_tests.py

# Run only memory addition tests
./run_latency_tests.py --test-type add

# Run only memory search tests
./run_latency_tests.py --test-type search

# Run tests with a custom number of iterations
./run_latency_tests.py --iterations 50

# Run tests with a specific OpenAI API key
./run_latency_tests.py --api-key YOUR_API_KEY

# Run tests with a custom database URL
./run_latency_tests.py --db-url postgresql://user:password@hostname:port/database

# Enable debug logging
./run_latency_tests.py --log-level DEBUG

# Don't save results to a file
./run_latency_tests.py --no-save
```

Alternatively, you can run the tests using pytest directly:

```bash
# Run all latency tests
pytest -xvs test_latency.py

# Run a specific test
pytest -xvs test_latency.py::test_add_memory_latency
```

### Test Results

The latency tests save results to JSON files with timestamps in the current directory. These files contain:

- Test configuration details (timestamp, iterations, database URL, etc.)
- Performance metrics for each test
- Raw latency data

Example results file:

```json
{
  "timestamp": "2023-05-21T12:34:56.789123",
  "test_type": "all",
  "iterations": 10,
  "database_url": "postgresql://memuri:memuri@localhost:5432/memuri",
  "embedding_model": "text-embedding-3-small",
  "tests": {
    "add_memory": {
      "min": 123.45,
      "max": 456.78,
      "mean": 234.56,
      "median": 222.33,
      "count": 10,
      "stdev": 45.67
    },
    "search_memory": {
      "min": 78.90,
      "max": 234.56,
      "mean": 123.45,
      "median": 111.22,
      "count": 10,
      "stdev": 23.45
    }
  }
}
```

### Interpreting Results

The latency tests provide statistics for each operation, including:

- Minimum latency
- Maximum latency
- Mean (average) latency
- Median latency
- Standard deviation (for statistical analysis)

A good performance baseline depends on your specific requirements, but generally:

- Add memory operations: <500ms is excellent, <1000ms is good
- Search memory operations: <200ms is excellent, <500ms is good

### Test Configuration

The latency tests use the following configuration by default:

- Provider: OpenAI
- Embedding model: text-embedding-3-small
- Vector store: pgvector (PostgreSQL with pgvector extension)
- Database URL: postgresql://memuri:memuri@localhost:5432/memuri

You can customize these settings by modifying the environment variables or using the command-line arguments.

## Other Tests

In addition to the latency tests, this directory also contains:

- **Unit tests**: Tests for individual components
- **Integration tests**: Tests for component interactions
- **Configuration fixtures**: Test fixtures and utilities 