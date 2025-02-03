# GitHub Repository Visualizer

A Python script that creates a visual representation of GitHub repository
structures. The script generates a directed graph visualization showing the
hierarchical structure of files and directories within a repository.

## Features

- Visualizes both public and private GitHub repositories
- Supports both HTTPS and SSH repository URLs
- Creates a hierarchical directed graph of the repository structure
- Color-codes directories and files for easy visualization
- Handles authentication via GitHub personal access tokens
- Includes detailed error handling and debugging capabilities

## Prerequisites

Before using this script, ensure you have the following installed:

- Python 3.6 or higher
- Graphviz (system dependency)
  - On Ubuntu/Debian: `sudo apt-get install graphviz`
  - On macOS: `brew install graphviz`
  - On Windows: Download and install from
    [Graphviz's official website](https://graphviz.org/download/)

## Required Python Packages

```bash
pip install PyGithub requests graphviz
```

## Setup

1. Clone or download the script to your local machine

2. Generate a GitHub Personal Access Token:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Click "Generate new token (classic)"
   - Select the following scopes:
     - `repo` (for private repositories)
   - Copy the generated token

## Usage

1. Basic usage:

```python
from repo_visualizer import visualize_github_repo

# For public repositories
visualize_github_repo(
    repo_url="https://github.com/username/repository",
    output_file="repo_visualization"
)

# For private repositories
visualize_github_repo(
    repo_url="https://github.com/username/repository",
    access_token="your_github_token",
    output_file="repo_visualization"
)
```

2. With debug mode enabled:

```python
visualize_github_repo(
    repo_url="https://github.com/username/repository",
    access_token="your_github_token",
    output_file="repo_visualization",
    debug=True
)
```

## Output

The script generates:

- A PNG file showing the repository structure visualization
- A DOT file (source file for the visualization)
- The visualization will automatically open in your default image viewer

## Visualization Legend

- Blue boxes: Directories
- White boxes: Files
- Arrows: Show the hierarchical relationships between files and directories

## Troubleshooting

1. **404 Error**:

   - Verify the repository URL is correct
   - Ensure you have access to the repository
   - Check if your token has the correct permissions

2. **Token Issues**:

   - Verify token has the `repo` scope for private repositories
   - Check if token has expired
   - For organization repositories, ensure the token has organization access

3. **Graphviz Errors**:
   - Ensure Graphviz is properly installed on your system
   - Add Graphviz to your system PATH if needed

## Limitations

- Cannot visualize repositories with a very large number of files (GitHub API
  limitation)
- Some binary files and special file types might be excluded
- Hidden files (starting with '.') are ignored by default

## Error Messages

Common error messages and their solutions:

- `404 {"message": "Not Found"}`:

  - Check repository URL
  - Verify token permissions
  - Ensure repository exists

- `401 {"message": "Bad credentials"}`:
  - Token is invalid or expired
  - Generate a new token

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for
any improvements.

## License

This project is licensed under the MIT License

## Acknowledgments

- Uses the PyGithub library for GitHub API interaction
- Uses Graphviz for visualization generation
