# RepoSpoofScanner 🔍🛡️

[![CI](https://github.com/yourusername/RepoSpoofScanner/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/RepoSpoofScanner/actions)
[![PyPI](https://img.shields.io/pypi/v/repospoofscanner)](https://pypi.org/project/repospoofscanner/)

A security scanner that detects malicious package dependencies in GitHub repositories through:
- **Typosquatting detection** (Levenshtein distance)
- **Registry validation** (npm/PyPI)
- **Suspicious code pattern scanning**

## Features ✨
- Async GitHub API client with rate limit handling
- Multi-registry support (npm, PyPI)
- Rich terminal output with progress tracking
- CI-ready with pre-commit hooks

## Quickstart 🚀
```bash
pip install repospoofscanner
repospoof scan https://github.com/user/repo --token your_gh_token
