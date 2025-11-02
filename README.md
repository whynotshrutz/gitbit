#GitBit

A comprehensive Python-based git repository management and version control operations agent.

## Features

- Clone repositories with branch-specific targeting
- Create and manage branches intelligently
- Handle git state and operation history
- Commit changes with descriptive messages
- Push branches with conflict resolution

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Usage

```python
from gitops.agents import GitOperationsAgent

# Initialize the agent
agent = GitOperationsAgent()

# Clone a repository
agent.clone_repository("https://github.com/user/repo.git", branch="main")

# Create a new branch
branch_name = agent.create_unique_branch("feature")

# Make changes and commit
agent.commit_changes("Add new feature")

# Push changes
agent.push_branch()

# Get repository status
status = agent.get_repository_status()
print(status)
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project uses black for code formatting:

```bash
black .
```

### Type Checking

```bash
mypy .
```
