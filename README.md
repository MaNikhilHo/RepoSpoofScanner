# RepoSpoofScanner 🔍🛡️

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
