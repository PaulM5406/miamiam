# Custom Instructions for GitHub Copilot

## Code Style Guidelines

1. Modern Python practices and idioms
2. Always use type hints
3. For typing, use native python types when available instead of typing module
4. Use dataclasses for data structures
5. Follow PEP 8
6. Use meaningful variable names
7. Add docstrings for public functions and classes
8. Keep functions focused and small
9. Use exception handling for API calls
10. Always use aware datetimes

## Common Patterns

1. Use dependency injection for clients and services
2. Implement strategy pattern for trading algorithms
3. Use dataclasses for data transfer objects

## Test Guidelines

1. Write pytest-style tests
2. Use fixtures for common test setups
3. Mock external API calls
4. Test edge cases and error conditions
5. Use parametrize for multiple test cases

## Error Handling

1. Use custom exceptions for domain-specific errors
2. Log errors with appropriate context
3. Gracefully handle API rate limits
4. Include retry mechanisms for transient failures

## Project Structure

```
maiamiam/
├── maiamiam/
│   ├── __init__.py
│   ├── file1.py
│   └── file2.py
├── tests/
│   └── ...
├── run.py             # Entry point
└── README.md
```
