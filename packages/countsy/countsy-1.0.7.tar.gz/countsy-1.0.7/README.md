# Countsy 📏

*A fast, customizable line counter for Python projects (with plans to expand!)*

## Features ✨

- Count lines in **Python files** (with more languages coming soon!)
- **Flexible filtering**: Ignore comments, blank lines, or both
- **Progress bars** (optional) for large directories
- Faster than `cloc` for pure Python projects

## Installation ⚡

```bash
pip install countsy
```

## Usage 🚀

### Basic Command

```bash
countsy /path/to/folder  # Default: current directory
```

### Sample Output

```
Total Python-Files: 1129
Total lines of Python-Code in folder: 376045
```

## Flags 🎛️

| Flag | Description | Default |
|------|-------------|---------|
| `--tqdm` | Show progress bar | False |
| `--ignore-comments` | Exclude single/multi-line comments | False |
| `--ignore-blank-lines` | Exclude empty lines | False |
| `--ignore` | Exclude both comments and blank lines | False |

### Example

```bash
countsy /path/to/folder --ignore --tqdm
```

## Disclaimer⚠️

- `tqdm` is required for progress bars

## Missing Modules? 🔧

```bash
# Install required dependencies
pip install tqdm
```

## Roadmap 🗺️

- Support for more languages (JavaScript, Java, etc.)
- Optimize speed for large codebases
- Optional dependencies

## Contributing 🤝

PRs and feature requests are welcome!