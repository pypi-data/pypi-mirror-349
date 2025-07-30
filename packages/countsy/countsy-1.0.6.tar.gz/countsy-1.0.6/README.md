# Countsy
This is countsy. Currently you can return the amount of lines for all Python-Files of an
entire dictionary. Via flags you have the option to ignore comments, blank lines or both.
I would like to work on optimization, although for pure python projects this is faster than cloc
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
countsy
>>> Total lines of Python-Code in folder:  86
```

### Flags
call countsy for help
```
folder_path: positional, right after countsy, optional with default set to current directory
--tqdm: includes progress bar, default is false
--ignore-comments: ignores all comments (single and multiline)
--ignore-blank-lines: ignores all blank lines
--ignore: ignores both comments and blank lines
```
### Disclaimer
The --ignore-blank-lines flag does not ignore blank lines inside of multiline comments. 
Both ignore flags are best used together (-> --ignore).