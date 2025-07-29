# Contributing to PreProPy

Thank you for your interest in contributing to PreProPy! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Fork the repository and clone your fork:
   ```bash
   git clone https://github.com/yourusername/prepropy.git
   cd prepropy
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Testing

Before submitting a pull request, make sure to run the tests:

```bash
python -m tests.run_tests
```

## Code Style

This project follows PEP 8 for code style. Please ensure your code adheres to these guidelines.

- Use 4 spaces for indentation
- Use docstrings for all functions, classes, and modules
- Maximum line length of 88 characters
- Add meaningful comments where necessary

## Pull Request Process

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Add or update tests as necessary
4. Run the test suite to ensure all tests pass
5. Submit a pull request to the main repository

## Feature Requests

If you have ideas for new features or improvements, please open an issue on GitHub to discuss them before submitting code.

## Bug Reports

If you find a bug, please open an issue on GitHub with the following information:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- Environment information (Python version, OS, package version)

## Code of Conduct

Please be respectful to all contributors and users. We aim to foster an inclusive and welcoming community.

Thank you for contributing to PreProPy!
