# Countsy
This is countsy. Currently you can return the amount of lines for all Python-Files of an
entire dictionary.
It does not ignore comments and or blank lines (probably following), also I would like to 
work on implementing more programming languages.
## Usage
### Installation
```
pip install countsy
```
### Usage
```
countsy FOLDER_TO_PATH
```

### Sample Output
```
countsy ./
>>> Total lines of Python-Code in folder:  86
```

### Flags
call countsy for help
```
folder_path: positional, right after countsy
--tqdm: includes progress bar, default is false
```